FROM node:22-slim

WORKDIR /app

# A imagem node já traz um usuário não-root dedicado (`node`, uid/gid 1000,
# casando com o usuário host nos bind mounts). Reutilizamos em vez de criar
# uma duplicata — mesmo objetivo da SEC-10 no backend, sem colisão de UID.
#
# O WORKDIR nasce como root: garante posse do node antes de descer privilégio,
# senão o npm não consegue criar node_modules/ dentro de /app
RUN chown node:node /app

# Os manifestos de pacote são copiados com dono correto e as dependências
# são instaladas já como não-root (node_modules precisa ser gravável pelo
# runtime: o Vite escreve cache em node_modules/.vite)
COPY --chown=node:node package*.json ./
USER node
RUN npm install

# Copia o restante dos arquivos do projeto
COPY --chown=node:node . .

# Expõe a porta do Vite
EXPOSE 5173

# Roda o servidor de desenvolvimento liberando o host para o Docker
CMD ["npm", "run", "dev", "--", "--host"]