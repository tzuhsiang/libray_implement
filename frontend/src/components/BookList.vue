<template>
  <div>
    <h2 class="text-xl font-semibold text-gray-800 mb-4">📖 書籍清單</h2>
    <div v-if="books.length === 0" class="bg-white rounded-lg shadow-lg p-12 text-center border-2 border-dashed border-gray-200">
      <div class="text-indigo-200 text-7xl mb-4">📚</div>
      <p class="text-gray-500 text-lg">目前書架沒有書籍，開始建立你的第一份書單吧！</p>
    </div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="book in books" :key="book.id" class="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow">
        <div class="p-6">
          <h3 class="text-lg font-bold text-gray-900 mb-2">{{ book.title }}</h3>
          <p class="text-sm text-gray-600 mb-3">作者：{{ book.author }}</p>
          <div class="mb-3 flex items-center space-x-1" @mouseleave="hoverRating = null">
            <button 
              v-for="star in 5" 
              :key="star" 
              type="button"
              @click="rateBook(book, star)"
              @mouseenter="hoverRating = { id: book.id, val: star }"
              class="focus:outline-none transition-transform hover:scale-110"
            >
              <span class="text-2xl transition-colors" 
                :class="(hoverRating?.id === book.id ? star <= hoverRating.val : star <= book.rating) ? 'text-yellow-400 drop-shadow-sm' : 'text-gray-200'">
                ★
              </span>
            </button>
          </div>
          <div class="mb-4">
            <select v-model="book.status" @change="updateBook(book)" class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500">
              <option value="unread">未讀</option>
              <option value="reading">閱讀中</option>
              <option value="finished">已完成</option>
            </select>
          </div>

          <button @click="deleteBook(book.id)" class="w-full px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-colors">🗑️ 刪除</button>
        </div>
        <div class="px-6 py-2 text-center text-sm font-medium" 
             :class="{
               'bg-slate-100 text-slate-600': book.status === 'unread',
               'bg-blue-100 text-blue-600': book.status === 'reading',
               'bg-emerald-100 text-emerald-600': book.status === 'finished'
             }">
          {{ statusText(book.status) }}
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { ref } from 'vue'
import axios from 'axios'
export default {
  name: 'BookList',
  props: { books: { type: Array, required: true } },
  emits: ['book-updated', 'book-deleted'],
  setup(props, { emit }) {
    const statusText = (status) => {
      const statusMap = { 'unread': '📕 未讀', 'reading': '📖 閱讀中', 'finished': '✅ 已完成' }
      return statusMap[status] ; status
    }
    const hoverRating = ref(null)
    
    // Debounce timer
    let debounceTimer = null

    const updateBookStatus = async (book) => {
      try {
        await axios.put(`/books/${book.id}`, { status: book.status, rating: book.rating })
        // Local update is automatic via v-model, no need to refresh
      } catch (error) {
        console.error('Failed to update status:', error)
        alert('狀態更新失敗')
      }
    }

    const rateBook = (book, star) => {
      // Optimistic update
      const oldRating = book.rating
      book.rating = star
      
      // Debounce API call
      if (debounceTimer) clearTimeout(debounceTimer)
      
      debounceTimer = setTimeout(async () => {
        try {
          await axios.put(`/books/${book.id}`, { status: book.status, rating: star })
        } catch (error) {
          // Revert on failure
          book.rating = oldRating
          console.error('Failed to update rating:', error)
          alert('評分更新失敗')
        }
      }, 500)
    }

    // Expose updateBook as alias for status change to keep template simple if needed, 
    // or just use updateBookStatus directly.
    // The template uses updateBook(book) for status select.
    const updateBook = updateBookStatus
    const deleteBook = async (bookId) => {
      if (!confirm('確定要刪除這本書嗎？')) return
      try {
        await axios.delete(`/books/${bookId}`)
        emit('book-deleted')
        alert('刪除成功！')
      } catch (error) {
        console.error('Failed to delete book:', error)
        alert('刪除失敗，請稍後再試')
      }
    }
    return { statusText, updateBook, deleteBook, rateBook, hoverRating }
  }
}
</script>
