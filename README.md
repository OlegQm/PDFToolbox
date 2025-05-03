# PDFToolbox

## Начало работы

### Необходимые компоненты
- [Git](https://git-scm.com/downloads)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Системные требования
- Свободное место: 5–8 ГБ
- Оперативная память: минимум 2 ГБ

## Установка и запуск

1. Клонировать репозиторий:
   `git clone https://github.com/OlegQm/PDFToolbox.git`
2. Перейти в папку проекта:
   `cd PDFToolbox`
3. Запустить контейнеры:
   `make up`  
4. Открыть в браузере:
   Фронтенд: `http://localhost:3001`  
   Бэкенд (API): `http://localhost:8000`  
   MongoDB: `mongodb://mongodb:27017/mydb`  
5. Остановить приложение:
   Ctrl + C (или `make down`)
6. Перезапустить приложение:

## Полезные команды

- `make clean_all`  
(при проблемах с Docker — переустановить Docker Desktop)
- `make logs`
(посмотреть логи приложения в Docker)
