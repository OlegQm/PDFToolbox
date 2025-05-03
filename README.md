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
   `docker compose up --build`
4. Открыть в браузере:
   Фронтенд: `http://localhost:3001`  
   Бэкенд (API): `http://localhost:8000`  
   MongoDB: `mongodb://mongodb:27017/mydb`  
5. Остановить приложение:
   Ctrl + C (или `docker compose down`)
6. Перезапустить приложение:
   `docker compose down && docker compose up --build`
## Полезные команды

- `docker compose down --volumes --remove-orphans
	docker system prune -a --volumes -f`
(при проблемах с Docker — переустановить Docker Desktop)
- `docker compose logs -f`
(посмотреть логи приложения в Docker)
