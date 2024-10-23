version: "3"
services:
  db:
    image: postgres
    environment:
      POSTGRES_DB: itstime
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: PaSSword
    volumes:
      - ./db_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
  redis:
    image: redis:latest
    container_name: redis
    ports:
      - "6379:6379"
  backend:
    build:
      context: ./Backend
      dockerfile: Dockerfile
    working_dir: /usr/itbu
    
    env_file:
      - ./Backend/.env
    volumes:
        - ./Backend:/usr/itbu
    expose:
      - 9006
    ports:
      - "9006:9006"
    environment:
      DATABASE_URL: postgres://admin:PaSSword@db:5432/itstime
      REDIS_HOST : redis
    depends_on:
      - db