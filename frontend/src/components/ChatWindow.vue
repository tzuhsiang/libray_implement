<template>
  <div>

    <!-- Chat Window Side Panel -->
    <transition name="slide-right">
      <div
        v-if="isOpen"
        class="fixed top-0 right-0 h-screen w-full sm:w-[33.333333%] bg-white shadow-2xl flex flex-col overflow-hidden border-l border-gray-200 z-[60]"
      >
        <div class="bg-indigo-600 p-4 flex justify-between items-center text-white">
            <span class="text-xl">🤖</span>
            <h3 class="font-bold">圖書助理 Agent</h3>
          </div>
          <div class="flex items-center gap-2">
            <button @click="resetChat" class="hover:text-gray-200 focus:outline-none" title="重啟對話">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                 <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd" />
              </svg>
            </button>
          <button @click="toggleChat" class="hover:text-gray-200 focus:outline-none">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>

        <div class="flex-1 p-4 overflow-y-auto bg-gray-50" ref="messagesRef">
          <div v-for="(msg, index) in messages" :key="index" class="mb-4 flex flex-col">
            <div :class="['max-w-[85%] rounded-2xl p-3 px-4', msg.role === 'user' ? 'bg-indigo-600 ml-auto text-white rounded-tr-none' : 'bg-white mr-auto text-gray-800 shadow-sm border border-gray-100 rounded-tl-none']">
              
              <!-- Thought Process Block for AI -->
              <div v-if="msg.thoughts && msg.thoughts.length > 0" class="mb-3">
                <details class="text-sm text-gray-500 bg-gray-50 rounded-lg p-2 border border-gray-100">
                  <summary class="cursor-pointer font-medium flex items-center gap-1 select-none">
                    <span v-if="msg.status === 'thinking'" class="animate-spin text-indigo-500 inline-block w-4 h-4 border-2 border-current border-t-transparent rounded-full mr-1"></span>
                    <span v-else>💡</span>
                    {{ msg.status === 'thinking' ? '思考與執行中...' : '已完成的工作流程' }}
                  </summary>
                  <ul class="mt-2 space-y-2">
                    <li v-for="thought in msg.thoughts" :key="thought.name" class="flex flex-col gap-1 border-l-2 border-indigo-200 pl-2 ml-1">
                      <div class="flex items-center gap-2">
                         <span v-if="thought.status === 'pending'" class="animate-spin text-indigo-500 inline-block w-3 h-3 border-2 border-current border-t-transparent rounded-full"></span>
                         <span v-else-if="thought.status === 'success'" class="text-green-500">✓</span>
                         <span class="font-mono text-xs text-indigo-700 font-semibold px-1 bg-indigo-50 rounded">🛠️ {{ thought.name }}</span>
                      </div>
                      <span v-if="thought.status === 'pending'" class="text-xs text-gray-400">執行中...</span>
                    </li>
                  </ul>
                </details>
              </div>

              <p class="whitespace-pre-wrap leading-relaxed">{{ msg.content }}</p>
            </div>
            <span :class="['text-xs text-gray-400 mt-1', msg.role === 'user' ? 'text-right' : 'text-left']">{{ msg.time }}</span>
          </div>
          <div v-if="isLoading" class="flex justify-start mb-4">
             <div class="bg-white rounded-2xl rounded-tl-none p-3 shadow-sm border border-gray-100 flex items-center gap-1">
                <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></span>
                <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></span>
                <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.4s"></span>
             </div>
          </div>
        </div>

        <div class="p-4 border-t border-gray-100 bg-white">
          <form @submit.prevent="sendMessage" class="flex gap-2">
            <input
              v-model="inputMessage"
              type="text"
              placeholder="輸入訊息..."
              class="flex-1 px-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
              :disabled="isLoading"
            />
            <button
              type="submit"
              class="bg-indigo-600 text-white p-2 rounded-full hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex-shrink-0"
              :disabled="isLoading || !inputMessage.trim()"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 transform rotate-90" viewBox="0 0 20 20" fill="currentColor">
                <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
              </svg>
            </button>
          </form>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { ref, nextTick, watch } from 'vue'
import axios from 'axios'

export default {
  name: 'ChatWindow',
  props: {
    isOpen: {
      type: Boolean,
      default: false
    }
  },
  emits: ['chat-updated', 'toggle-chat'],
  setup(props, { emit }) {
    const inputMessage = ref('')
    const messages = ref([
      { 
        role: 'assistant', 
        content: '您好！我是您的圖書管理助理。您可以請我幫忙新增、查詢或修改書籍。',
        thoughts: [],
        status: 'done',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }
    ])
    const isLoading = ref(false)
    const messagesRef = ref(null)

    const toggleChat = () => {
      emit('toggle-chat')
    }

    // Watch for isOpen to auto-scroll when opened
    watch(() => props.isOpen, (newVal) => {
      if (newVal) {
        scrollToBottom()
      }
    })

    const scrollToBottom = async () => {
      await nextTick()
      if (messagesRef.value) {
        messagesRef.value.scrollTop = messagesRef.value.scrollHeight
      }
    }

    const resetChat = () => {
      messages.value = [
        { 
          role: 'assistant', 
          content: '您好！我是您的圖書管理助理。您可以請我幫忙新增、查詢或修改書籍。',
          thoughts: [],
          status: 'done',
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]
    }

    const sendMessage = async () => {
      if (!inputMessage.value.trim() || isLoading.value) return

      const userMsg = inputMessage.value
      messages.value.push({ 
        role: 'user', 
        content: userMsg,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      })
      inputMessage.value = ''
      isLoading.value = true
      scrollToBottom()

      const assistantMsg = {
        role: 'assistant',
        content: '',
        thoughts: [],
        status: 'thinking',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }
      messages.value.push(assistantMsg)

      try {
        const apiUrl = import.meta.env.VITE_API_URL === 'http://localhost:8000' ? '/api' : (import.meta.env.VITE_API_URL || '/api');
        const response = await fetch(`${apiUrl}/chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ message: userMsg })
        });

        if (!response.ok) {
           throw new Error(`HTTP error! status: ${response.status}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');
        let done = false;
        let buffer = '';

        while (!done) {
          const { value, done: readerDone } = await reader.read();
          done = readerDone;
          
          if (value) {
            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n\n');
            buffer = lines.pop() || ''; // Keep incomplete part in buffer
            
            for (const line of lines) {
              if (line.startsWith('data: ')) {
                const dataStr = line.substring(6); // remove 'data: '
                try {
                  const event = JSON.parse(dataStr);
                  
                  if (event.type === 'agent_start') {
                    // Start the thought process block immediately with a generic analysis task
                    assistantMsg.thoughts.push({
                      name: '分析任務與意圖',
                      args: {},
                      status: 'pending'
                    });
                  } else if (event.type === 'tool_start') {
                    // Mark analysis as successful once concrete tools start
                    const firstThought = assistantMsg.thoughts.find(t => t.name === '分析任務與意圖' && t.status === 'pending');
                    if (firstThought) firstThought.status = 'success';

                    assistantMsg.thoughts.push({
                      name: event.name,
                      args: event.args,
                      status: 'pending'
                    });
                  } else if (event.type === 'tool_end') {
                    const thoughtReversed = [...assistantMsg.thoughts].reverse();
                    const pendingThought = thoughtReversed.find(t => t.name === event.name && t.status === 'pending');
                    if (pendingThought) {
                      pendingThought.status = event.result === 'success' ? 'success' : 'error';
                    }
                    
                    if (['add_book', 'delete_book', 'update_book_rating', 'update_book_status'].includes(event.name)) {
                      emit('chat-updated');
                    }
                  } else if (event.type === 'message_chunk') {
                    // Ensure analysis is resolved if no tools were called
                    const firstThought = assistantMsg.thoughts.find(t => t.name === '分析任務與意圖' && t.status === 'pending');
                    if (firstThought) firstThought.status = 'success';

                    assistantMsg.content += event.content || '';
                  } else if (event.type === 'done' || event.type === 'error') {
                    const firstThought = assistantMsg.thoughts.find(t => t.name === '分析任務與意圖' && t.status === 'pending');
                    if (firstThought) firstThought.status = 'success';
                    assistantMsg.status = 'done';
                  }
                  
                  scrollToBottom();
                } catch (e) {
                  console.error('Error parsing SSE event:', e, dataStr);
                }
              }
            }
          }
        }
      } catch (error) {
        console.error('Chat error:', error);
        assistantMsg.content += '\n\n[系統連線異常，請稍後再試。]';
        assistantMsg.status = 'done';
      } finally {
        assistantMsg.status = 'done';
        isLoading.value = false;
        scrollToBottom();
      }
    }

    return { inputMessage, messages, isLoading, toggleChat, sendMessage, messagesRef, resetChat }
  }
}
</script>

<style scoped>
.slide-right-enter-active,
.slide-right-leave-active {
  transition: transform 0.3s ease-in-out, opacity 0.3s ease-in-out;
}

.slide-right-enter-from,
.slide-right-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
</style>
