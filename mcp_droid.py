#!/usr/bin/env python3
import asyncio
import sys
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent
import phone_util as pu

# 创建服务器实例
app = Server("android-mcp")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """list all tools"""
    return [
        Tool(
            name="app_list",
            description="list all apps in android phone",
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
        ),
        Tool(
            name="dump_hierarchy",
            description="dump current page hierarchy",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_current_page",
            description="get current page picture",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="click",
            description="Click pixel coordinates",
            inputSchema={
                "type": "object",
                "properties": {
                    "click_type": {
                        "type": "string",
                        "description": "this click type should be click, double_click, long_click. only the three value",
                    },
                    "x": {
                        "type": "integer",
                        "description": "x-coordinate",
                    },
                    "y": {
                        "type": "integer",
                        "description": "y-coordinate",
                    },

                },
                "required": ["click_type", "x", "y"]
            }
        ),
        Tool(
            name="interact_with_element",
            description="get and manipulate element",
            inputSchema={
                "type": "object",
                "properties": {
                    "resource_id": {
                        "type": "string",
                        "description": "the element resource id",
                    },
                    "operation": {
                        "type": "string",
                        "description": "how to manipulate element, there have some value like: click, long_click, clear_text, set_text",
                    },
                    "operation_value": {
                        "type": "string",
                        "description": "some operation need value, so here is the value",
                    },

                },
                "required": ["resource_id", "operation"]
            }
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """call tool"""

    match name:
        case "app_list":
            try:
                result = str(pu.app_list())
                return [TextContent(type="text", text=result or "no device")]
            except Exception as e:
                return [TextContent(type="text", text=f"执行失败: {str(e)}")]
        case "app_start":
            package = arguments.get("package")
            if not package:
                return [TextContent(type="text", text="错误: 缺少 package 参数")]
            try:
                pu.app_start(package)
                return [TextContent(type="text", text="start success")]
            except Exception as e:
                return [TextContent(type="text", text=f"执行失败: {str(e)}")]
        case "dump_hierarchy":
            result = str(pu.dump_hierarchy())
            return [TextContent(type="text", text=result or "no device")]
        case "get_current_page":
            result = pu.get_current_page()
            return [ImageContent(type="image", data=result, mimeType="image/png")]
        case "click":
            click_type = arguments.get("click_type")
            x = arguments.get("x")
            y = arguments.get("y")
            pu.click(click_type, x, y)
            return [TextContent(type="text", text="click success")]
        case "interact_with_element":
            resource_id = arguments.get("resource_id")
            operation = arguments.get("operation")
            operation_value = arguments.get("operation_value")
            pu.interact_with_element(resource_id, operation, operation_value)
            return [TextContent(type="text", text="done success")]

        case _:
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