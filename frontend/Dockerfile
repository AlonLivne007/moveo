FROM node:18-alpine

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

# Source will be mounted as a volume in docker-compose for hot reload,
# but we copy once so the image can start even before the volume is attached.
COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
