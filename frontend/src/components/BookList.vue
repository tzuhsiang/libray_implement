<template>
  <div>
    <h2 class="text-xl font-semibold text-gray-800 mb-4">📖 書籍清單</h2>
    <div v-if="books.length === 0" class="bg-white rounded-lg shadow p-12 text-center">
      <div class="text-gray-400 text-6xl mb-4">📚</div>
      <p class="text-gray-500">目前還沒有任何書籍，快來新增第一本書吧！</p>
    </div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="book in books" :key="book.id" class="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow">
        <div class="p-6">
          <h3 class="text-lg font-bold text-gray-900 mb-2">{{ book.title }}</h3>
          <p class="text-sm text-gray-600 mb-3">作者：{{ book.author }}</p>
          <div class="mb-3">
            <div class="flex items-center space-x-1">
              <span v-for="star in 5" :key="star" class="text-xl" :class="star <= book.rating ? 'text-yellow-400' : 'text-gray-300'">★</span>
            </div>
          </div>
          <div class="mb-4">
            <select v-model="book.status" @change="updateBook(book)" class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500">
              <option value="unread">未讀</option>
              <option value="reading">閱讀中</option>
              <option value="finished">已完成</option>
            </select>
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">更新評分</label>
            <input v-model.number="book.rating" @change="updateBook(book)" type="number" min="0" max="5" class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500" />
          </div>
          <button @click="deleteBook(book.id)" class="w-full px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-colors">🗑️ 刪除</button>
        </div>
        <div class="px-6 py-2 text-center text-sm font-medium" :class="{'bg-gray-100 text-gray-700': book.status === 'unread','bg-blue-100 text-blue-700': book.status === 'reading','bg-green-100 text-green-700': book.status === 'finished'}">{{ statusText(book.status) }}</div>
      </div>
    </div>
  </div>
</template>
<script>
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
    const updateBook = async (book) => {
      try {
        await axios.put(`/books/${book.id}`, { status: book.status, rating: book.rating })
        emit('book-updated')
      } catch (error) {
        console.error('Failed to update book:', error)
        alert('更新失敗，請稍後再試')
      }
    }
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
    return { statusText, updateBook, deleteBook }
  }
}
</script>
