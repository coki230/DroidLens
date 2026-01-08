#!/usr/bin/env python3
import asyncio
import sys
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import phone_util as pu

# 创建服务器实例
app = Server("android-mcp")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """list all tools"""
    return [
        Tool(
            name="app_list_running",
            description="list all running apps in android phone",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="app_start",
            description="start app in android phone",
            inputSchema={
                "type": "object",
                "properties": {
                    "package": {
                        "type": "string",
                        "description": "the app's package name",
                    }
                },
                "required": ["package"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """call tool"""

    if name == "app_list_running":
        try:
            result = str(pu.app_list_running())
            return [TextContent(type="text", text=result or "无设备连接")]
        except Exception as e:
            return [TextContent(type="text", text=f"执行失败: {str(e)}")]

    elif name == "app_start":
        package = arguments.get("package")
        if not package:
            return [TextContent(type="text", text="错误: 缺少 package 参数")]

        try:
            result = pu.app_start(package)
            return [TextContent(type="text", text="start success")]
        except Exception as e:
            return [TextContent(type="text", text=f"执行失败: {str(e)}")]

    else:
        return [TextContent(type="text", text=f"未知工具: {name}")]


async def main():
    """主函数：启动 stdio 服务器"""
    # 将调试信息输出到 stderr
    print("Android MCP Server starting...", file=sys.stderr)

    async with stdio_server() as (read_stream, write_stream):
        print("Server connected via stdio", file=sys.stderr)
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server shutdown", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)