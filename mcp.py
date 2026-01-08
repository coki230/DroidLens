#!/usr/bin/env python3
import json
import sys
import logging
import phone_util as pu
import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(script_dir, "mcp.log")
logging.basicConfig(level=logging.DEBUG, filename=log_file)

while True:
    try:
        line = sys.stdin.readline()
        if not line:
            break

        logging.info(line)

        # 解析请求
        req = json.loads(line)
        method = req.get("method", "")
        req_id = req.get("id")

        # 如果是通知消息（没有 id），直接跳过，不需要响应
        if req_id is None:
            # 完全不输出任何内容，包括到 stderr
            continue

        # 处理需要响应的请求
        if method == "initialize":
            res = {
                "protocolVersion": "2026-01-08",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "android mcp", "version": "1.0"}
            }
        elif method == "tools/list":
            res = {
                "tools": [
                    {
                        "name": "app_list_running",
                        "description": "list all running apps",
                        "inputSchema": {}
                    },
                    {
                        "name": "app_start",
                        "description": "start the app",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "package": {
                                    "type": "string",
                                    "description": "the package name of the app"
                                }
                            },
                            "required": ["package"]
                        }
                    }
                ]
            }
        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name", "")
            if tool_name == "app_list_running":
                run_list = pu.app_list_running()
                res = {"content": [{"type": "text", "text": run_list}]}
            else:
                res = {"error": {"code": -32601, "message": f"Unknown tool: {tool_name}"}}
        else:
            res = {"error": {"code": -32601, "message": f"Unknown method: {method}"}}

        # 发送响应（只对有 id 的请求响应）
        response = {"jsonrpc": "2.0", "id": req_id, "result": res}
        print(json.dumps(response), flush=True)

    except Exception:
        # 静默处理错误，不输出任何内容
        pass