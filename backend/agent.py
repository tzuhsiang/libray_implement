import os
import asyncio
from dataclasses import dataclass
from mcp import StdioServerParameters, ClientSession
from mcp.client.stdio import stdio_client
from pydantic_ai import Agent, RunContext
import nest_asyncio

# Apply nest_asyncio to allow nested event loops if needed
nest_asyncio.apply()

@dataclass
class McpDeps:
    session: ClientSession

# Initialize Agent
# Ensure env vars for Azure OpenAI are set (AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_VERSION)
# The model name is passed in the constructor.
agent = Agent(
    f'azure:{os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4o")}',
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
    server_script = os.path.join(os.path.dirname(__file__), "mcp_server.py")
    
    server_params = StdioServerParameters(
        command="python",
        args=[server_script],
        env=os.environ.copy()
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            deps = McpDeps(session=session)
            result = await agent.run(user_message, deps=deps)
            return result.output
