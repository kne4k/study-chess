# Imagem leve do Node.js
FROM node:20-alpine

# Pasta de trabalho
WORKDIR /app

# Copiar os arquivos de dependências
COPY package*.json ./

# Instalar as dependências
RUN npm install

# Copiar todo o código
COPY . .

# Porta onde o Vite roda
EXPOSE 5173

# Comandos
CMD ["npm", "run", "dev","--", "--host"]