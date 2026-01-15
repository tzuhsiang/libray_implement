import { createApp } from 'vue'
import axios from 'axios'
import App from './App.vue'
import './style.css'

// 設定 Axios 基礎 URL
const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
axios.defaults.baseURL = apiUrl

// 將 axios 掛載到全域屬性
const app = createApp(App)
app.config.globalProperties.$axios = axios

app.mount('#app')
