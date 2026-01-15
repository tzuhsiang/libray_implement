# 使用 Node.js 20 Alpine 映像檔
FROM node:20-alpine

# 設定工作目錄
WORKDIR /app

# 接收 build args
ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG NO_PROXY

# 設定 npm proxy（如果有的話）
RUN if [ -n "$HTTP_PROXY" ]; then npm config set proxy $HTTP_PROXY; fi ; \
    if [ -n "$HTTPS_PROXY" ]; then npm config set https-proxy $HTTPS_PROXY; fi

# 複製 package.json 和 package-lock.json
COPY package*.json ./

# 安裝依賴套件
RUN npm install

# 複製所有檔案
COPY . .

# 開放 5173 埠
EXPOSE 5173

# 啟動開發伺服器
CMD ["npm", "run", "dev"]
