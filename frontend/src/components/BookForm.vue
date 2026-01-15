<template>
  <div class="bg-white rounded-lg shadow-lg p-6 mb-6">
    <div v-if="!isExpanded" class="flex justify-center">
      <button @click="isExpanded = true" class="w-full md:w-auto px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 shadow-md transition-all flex items-center justify-center space-x-2">
        <span class="text-xl">➕</span>
        <span>新增書籍</span>
      </button>
    </div>
    <div v-else class="transition-all duration-300 ease-in-out">
      <div class="flex justify-between items-center mb-4 border-b pb-2">
        <h2 class="text-xl font-semibold text-gray-800">➕ 新增書籍</h2>
        <button @click="isExpanded = false" class="text-gray-500 hover:text-gray-700">
          ✕ 取消
        </button>
      </div>
    <form @submit.prevent="addBook" class="space-y-4">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">書名</label>
          <input v-model="form.title" type="text" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent" placeholder="請輸入書名" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">作者</label>
          <input v-model="form.author" type="text" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent" placeholder="請輸入作者" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">閱讀狀態</label>
          <select v-model="form.status" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
            <option value="unread">未讀</option>
            <option value="reading">閱讀中</option>
            <option value="finished">已完成</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">評分 (0-5)</label>
          <input v-model.number="form.rating" type="number" min="0" max="5" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent" placeholder="0-5 星" />
        </div>
      </div>
      <button type="submit" class="w-full md:w-auto px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors">新增書籍</button>
    </form>
    </div>
  </div>
</template>
<script>
import { ref } from 'vue'
import axios from 'axios'
export default {
  name: 'BookForm',
  emits: ['book-added'],
  setup(props, { emit }) {
    const isExpanded = ref(false)
    const form = ref({ title: '', author: '', status: 'unread', rating: 0 })
    const addBook = async () => {
      try {
        await axios.post('/books', form.value)
        form.value = { title: '', author: '', status: 'unread', rating: 0 }
        isExpanded.value = false
        emit('book-added')
        alert('書籍新增成功！')
      } catch (error) {
        console.error('Failed to add book:', error)
        alert('新增書籍失敗，請稍後再試')
      }
    }
    return { form, addBook, isExpanded }
  }
}
</script>
