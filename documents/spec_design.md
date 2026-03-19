# Frontend CoT (Chain of Thought) UI Specification

## 1. Objective
Implement real-time Chain of Thought (CoT) UI in the frontend, displaying intermediary tool calls dynamically before the final response.

## 2. API Communication Protocol
- **Transport**: Server-Sent Events (SSE) via FastAPI `StreamingResponse`.
- **Event Schema (JSON)**:
  - `{"type": "tool_start", "name": "add_book", "args": {"title": "..."}}`
  - `{"type": "tool_end", "name": "add_book", "result": "success"}`
  - `{"type": "message_chunk", "content": "..."}`
  - `{"type": "done"}`

## 3. Backend Implementation (`backend/agent.py` & `main.py`)
- **Agent Execution**: Modify `process_message` to use `agent.run_stream` or emit events via a callback mechanism.
- **Endpoint**: Change `/chat` endpoint from synchronous `return result.output` to asynchronous stream generator yielding JSON events.

## 4. Frontend State Models (`frontend/src/components/ChatWindow.vue`)
- **Message Interface**:
  ```typescript
  interface Message {
    id: string;
    role: 'user' | 'assistant';
    content: string;           // Final generated text chunks appended here
    thoughts: Thought[];       // Intermediary reasoning/tools
    status: 'thinking' | 'done';
  }

  interface Thought {
    id: string;
    type: 'tool';
    name: string;              // e.g. "add_book"
    args: any;
    status: 'pending' | 'success' | 'error';
  }
  ```

## 5. Frontend UI/UX Requirements
1. **Network Layer**: Replace `axios.post` with `fetch()` interacting with Web Streams API (reading `ReadableStream`), or raw `EventSource`.
2. **CoT Rendering (Thought Block)**:
   - Render `thoughts` above `content`.
   - Show a spinner/loading animation for `status: 'pending'`.
   - Show checkmark for `status: 'success'`.
   - Collapsible UI: Use `<details>` and `<summary>` for compacting past thoughts.
3. **Auto-Scrolling**: Automatically scroll to `.chat-container` bottom on every chunk update.
4. **Trigger Lifecycle**: If a mutating tool (e.g., `add_book`, `delete_book`) triggers a `tool_end` event, dispatch an event (e.g., `@chat-updated`) to `App.vue` to refresh the main book list dynamically.
