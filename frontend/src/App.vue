<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
    <header class="bg-white shadow-md">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <h1 class="text-3xl font-bold text-indigo-600">📚 LibriFlow</h1>
        <p class="text-gray-600 mt-1">個人圖書管理系統</p>
      </div>
    </header>
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="mb-8">
        <BookForm @book-added="fetchBooks" />
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div class="bg-white rounded-lg shadow p-6">
          <div class="text-sm text-gray-600">總書籍數</div>
          <div class="text-3xl font-bold text-indigo-600">{{ books.length }}</div>
        </div>
        <div class="bg-white rounded-lg shadow p-6">
          <div class="text-sm text-gray-600">閱讀中</div>
          <div class="text-3xl font-bold text-blue-600">{{ readingCount }}</div>
        </div>
        <div class="bg-white rounded-lg shadow p-6">
          <div class="text-sm text-gray-600">已完成</div>
          <div class="text-3xl font-bold text-green-600">{{ finishedCount }}</div>
        </div>
      </div>
      <BookList :books="books" @book-updated="fetchBooks" @book-deleted="fetchBooks" />
    </main>
  </div>
</template>
<script>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import BookForm from './components/BookForm.vue'
import BookList from './components/BookList.vue'
export default {
  name: 'App',
  components: { BookForm, BookList },
  setup() {
    const books = ref([])
    const readingCount = computed(() => books.value.filter(book => book.status === 'reading').length)
    const finishedCount = computed(() => books.value.filter(book => book.status === 'finished').length)
    const fetchBooks = async () => {
      try {
        const response = await axios.get('/books')
        books.value = response.data
      } catch (error) {
        console.error('Failed to fetch books:', error)
        alert('無法載入書籍清單，請檢查後端連線')
      }
    }
    onMounted(() => { fetchBooks() })
    return { books, readingCount, finishedCount, fetchBooks }
  }
}
</script>
