<template>
  <div class="fixed bottom-4 right-4 z-50">
    <!-- Chat Button -->
    <button
      v-if="!isOpen"
      @click="toggleChat"
      class="bg-indigo-600 hover:bg-indigo-700 text-white rounded-full p-4 shadow-lg transition-all duration-300 transform hover:scale-105 flex items-center justify-center"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
      </svg>
    </button>

    <!-- Chat Window -->
    <transition name="fade">
      <div
        v-if="isOpen"
        class="bg-white rounded-lg shadow-2xl w-[90vw] sm:w-[48rem] flex flex-col overflow-hidden border border-gray-200"
        style="height: 800px; max-height: 90vh;"
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
import { ref, nextTick } from 'vue'
import axios from 'axios'

export default {
  name: 'ChatWindow',
  emits: ['chat-updated'],
  setup(props, { emit }) {
    const isOpen = ref(false)
    const inputMessage = ref('')
    const messages = ref([
      { 
        role: 'assistant', 
        content: '您好！我是您的圖書管理助理。您可以請我幫忙新增、查詢或修改書籍。',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }
    ])
    const isLoading = ref(false)
    const messagesRef = ref(null)

    const toggleChat = () => {
      isOpen.value = !isOpen.value
      if (isOpen.value) {
        scrollToBottom()
      }
    }

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

      try {
        const response = await axios.post('/chat', { message: userMsg })
        messages.value.push({ 
          role: 'assistant', 
          content: response.data.reply,
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        })
        // Notify parent to refresh books
        emit('chat-updated')
      } catch (error) {
        console.error('Chat error:', error)
        messages.value.push({ 
          role: 'assistant', 
          content: '抱歉，發生錯誤，請稍後再試。',
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        })
      } finally {
        isLoading.value = false
        scrollToBottom()
      }
    }

    return { isOpen, inputMessage, messages, isLoading, toggleChat, sendMessage, messagesRef, resetChat }
  }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>
