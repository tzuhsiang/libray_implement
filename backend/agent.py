import os
import asyncio
import json
from dataclasses import dataclass
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from pydantic_ai import Agent, RunContext
import nest_asyncio

nest_asyncio.apply()

@dataclass
class McpDeps:
    session: ClientSession
    event_queue: asyncio.Queue = None

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
    if ctx.deps.event_queue:
        await ctx.deps.event_queue.put({"type": "tool_start", "name": "list_books", "args": {"limit": limit, "offset": offset}})
        
    result = await ctx.deps.session.call_tool("list_books", arguments={"limit": limit, "offset": offset})
    
    if ctx.deps.event_queue:
        await ctx.deps.event_queue.put({"type": "tool_end", "name": "list_books", "result": "success"})
        
    return result.content[0].text

@agent.tool
async def add_book(ctx: RunContext[McpDeps], title: str, author: str, status: str = "unread", rating: int = 0) -> str:
    """新增書籍 (status: unread, reading, finished)"""
    if ctx.deps.event_queue:
        await ctx.deps.event_queue.put({"type": "tool_start", "name": "add_book", "args": {"title": title, "author": author, "status": status, "rating": rating}})
        
    result = await ctx.deps.session.call_tool("add_book", arguments={
        "title": title, "author": author, "status": status, "rating": rating
    })
    
    if ctx.deps.event_queue:
        await ctx.deps.event_queue.put({"type": "tool_end", "name": "add_book", "result": "success"})
        
    return result.content[0].text

@agent.tool
async def delete_book(ctx: RunContext[McpDeps], book_id: int) -> str:
    """刪除書籍"""
    if ctx.deps.event_queue:
        await ctx.deps.event_queue.put({"type": "tool_start", "name": "delete_book", "args": {"book_id": book_id}})
        
    result = await ctx.deps.session.call_tool("delete_book", arguments={"book_id": book_id})
    
    if ctx.deps.event_queue:
        await ctx.deps.event_queue.put({"type": "tool_end", "name": "delete_book", "result": "success"})
        
    return result.content[0].text

@agent.tool
async def update_book_rating(ctx: RunContext[McpDeps], book_id: int, rating: int) -> str:
    """修改書本評價 (0-5)"""
    if ctx.deps.event_queue:
        await ctx.deps.event_queue.put({"type": "tool_start", "name": "update_book_rating", "args": {"book_id": book_id, "rating": rating}})
        
    result = await ctx.deps.session.call_tool("update_book_rating", arguments={"book_id": book_id, "rating": rating})
    
    if ctx.deps.event_queue:
        await ctx.deps.event_queue.put({"type": "tool_end", "name": "update_book_rating", "result": "success"})
        
    return result.content[0].text

@agent.tool
async def update_book_status(ctx: RunContext[McpDeps], book_id: int, status: str) -> str:
    """修改閱讀狀態 (unread, reading, finished)"""
    if ctx.deps.event_queue:
        await ctx.deps.event_queue.put({"type": "tool_start", "name": "update_book_status", "args": {"book_id": book_id, "status": status}})
        
    result = await ctx.deps.session.call_tool("update_book_status", arguments={"book_id": book_id, "status": status})
    
    if ctx.deps.event_queue:
        await ctx.deps.event_queue.put({"type": "tool_end", "name": "update_book_status", "result": "success"})
        
    return result.content[0].text

async def stream_message(user_message: str):
    """
    提供 Server-Sent Events 的訊息流，包含中間工具的執行步驟與最終文字。
    """
    event_queue = asyncio.Queue()

    async def run_agent_task():
        # 立刻送出 agent_start 事件，讓前端建立初步的「分析意圖」UI
        await event_queue.put({"type": "agent_start"})

        # 連接到 MCP Server 的 HTTP 端點 (FastMCP streamable-http 使用 /mcp)
        url = os.getenv("MCP_SERVER_URL", "http://mcp_server:8001/mcp")
        
        # 檢查並清理 Azure OpenAI Endpoint
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")
        if "/openai/deployments/" in azure_endpoint:
            os.environ["AZURE_OPENAI_ENDPOINT"] = azure_endpoint.split("/openai/deployments/")[0]

        # 強制略過代理伺服器
        os.environ.pop("HTTP_PROXY", None)
        os.environ.pop("HTTPS_PROXY", None)
        
        import httpx
        transport = httpx.AsyncHTTPTransport(proxy=None)

        try:
            async with streamable_http_client(url, http_client=httpx.AsyncClient(transport=transport)) as (read, write, _):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    deps = McpDeps(session=session, event_queue=event_queue)
                    
                    async with agent.run_stream(user_message, deps=deps) as result:
                        async for text_delta in result.stream_text(delta=True):
                            await event_queue.put({"type": "message_chunk", "content": text_delta})
                            
            await event_queue.put({"type": "done"})
        except Exception as e:
            import traceback
            error_msg = f"Agent process error: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            # 發生錯誤時先傳遞錯誤文字，再結束串流
            await event_queue.put({"type": "message_chunk", "content": f"\n\n抱歉，系統發生錯誤：{str(e)}"})
            await event_queue.put({"type": "error", "content": str(e)})

    # 在背景啟動 agent 執行
    asyncio.create_task(run_agent_task())

    # 負責將 Queue 內的事件轉為 SSE 格式送出
    while True:
        event = await event_queue.get()
        yield f"data: {json.dumps(event)}\n\n"
        
        if event["type"] in ("done", "error"):
            break

