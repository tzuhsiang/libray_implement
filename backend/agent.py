import os
import asyncio
from dataclasses import dataclass
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from pydantic_ai import Agent, RunContext
import nest_asyncio

nest_asyncio.apply()

@dataclass
class McpDeps:
    session: ClientSession

# Initialize Agent
agent = Agent(
    f'azure:{os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4.1")}',
    deps_type=McpDeps,
    system_prompt="""
    你是一個圖書管理助理。
    你可以協助使用者新增、查詢、修改、刪除書籍。
    
    支援的功能：
    - 新增書籍 (add_book)
    - 刪除書籍 (delete_book)
    - 修改評價 (update_book_rating)
    - 修改閱讀狀態 (update_book_status)
    - 列出書籍 (list_books)
    
    書籍狀態 (status) 只能是以下之一：unread (未讀), reading (閱讀中), finished (已讀)。
    
    請使用提供的工具執行操作。請用繁體中文回答。
    """
)

@agent.tool
async def list_books(ctx: RunContext[McpDeps], limit: int = 20, offset: int = 0) -> str:
    """列出書籍清單"""
    result = await ctx.deps.session.call_tool("list_books", arguments={"limit": limit, "offset": offset})
    return result.content[0].text

@agent.tool
async def add_book(ctx: RunContext[McpDeps], title: str, author: str, status: str = "unread", rating: int = 0) -> str:
    """新增書籍 (status: unread, reading, finished)"""
    result = await ctx.deps.session.call_tool("add_book", arguments={
        "title": title, "author": author, "status": status, "rating": rating
    })
    return result.content[0].text

@agent.tool
async def delete_book(ctx: RunContext[McpDeps], book_id: int) -> str:
    """刪除書籍"""
    result = await ctx.deps.session.call_tool("delete_book", arguments={"book_id": book_id})
    return result.content[0].text

@agent.tool
async def update_book_rating(ctx: RunContext[McpDeps], book_id: int, rating: int) -> str:
    """修改書本評價 (0-5)"""
    result = await ctx.deps.session.call_tool("update_book_rating", arguments={"book_id": book_id, "rating": rating})
    return result.content[0].text

@agent.tool
async def update_book_status(ctx: RunContext[McpDeps], book_id: int, status: str) -> str:
    """修改閱讀狀態 (unread, reading, finished)"""
    result = await ctx.deps.session.call_tool("update_book_status", arguments={"book_id": book_id, "status": status})
    return result.content[0].text

async def process_message(user_message: str):
    # 連接到 MCP Server 的 HTTP 端點 (FastMCP streamable-http 使用 /mcp)
    url = os.getenv("MCP_SERVER_URL", "http://mcp_server:8001/mcp")
    
    # 檢查並清理 Azure OpenAI Endpoint (pydantic-ai 需要 base URL)
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    if "/openai/deployments/" in azure_endpoint:
        # 如果使用者填入的是完整路徑，我們只取 base 部分
        os.environ["AZURE_OPENAI_ENDPOINT"] = azure_endpoint.split("/openai/deployments/")[0]

    # 強制略過代理伺服器（預防容器內部通訊被攔截）
    # 在此 process 中暫時移除代理設定，確保 OpenAI 和 MCP 都能直連
    os.environ.pop("HTTP_PROXY", None)
    os.environ.pop("HTTPS_PROXY", None)
    
    import httpx
    transport = httpx.AsyncHTTPTransport(proxy=None)

    try:
        # 使用自定義 transport 建立 streamable_http_client
        # 修正參數名稱為 http_client
        async with streamable_http_client(url, http_client=httpx.AsyncClient(transport=transport)) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                deps = McpDeps(session=session)
                result = await agent.run(user_message, deps=deps)
                return result.output
    except Exception as e:
        import traceback
        error_msg = f"Agent process error: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)  # 這將會顯示在 docker logs 中
        return f"抱歉，系統發生錯誤：{str(e)}"

