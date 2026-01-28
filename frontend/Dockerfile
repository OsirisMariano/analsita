FROM node:22-slim

WORKDIR /app

# Copia os arquivos de definição de pacotes
COPY package*.json ./

# Instala as dependências
RUN npm install

# Copia o restante dos arquivos do projeto
COPY . .

# Expõe a porta do Vite
EXPOSE 5173

# Roda o servidor de desenvolvimento liberando o host para o Docker
CMD ["npm", "run", "dev", "--", "--host"]