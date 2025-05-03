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
    4.1. Фронтенд:
        - Локально: `http://localhost:3001`
        - На сервере: `https://node100.webte.fei.stuba.sk/PDFToolbox/`
    4.2. Бэкенд (API):
        - Локально: `http://localhost:8000/api` (`http://localhost:8000/api/docs`, если нужна документация)
        - На сервере: `https://node100.webte.fei.stuba.sk/PDFToolbox/api` (`https://node100.webte.fei.stuba.sk/PDFToolbox/api/docs`, если нужна документация)
    4.3. MongoDB:
        - URI: `mongodb://mongodb:27017/mydb` 
6. Остановить приложение:
   Ctrl + C (или `docker compose down`)
7. Перезапустить приложение:
   `docker compose down && docker compose up --build`

## Полезные команды
#### Очистить файлы Docker-а
- `docker compose down --volumes --remove-orphans`
- `docker system prune -a --volumes -f`
- При проблемах с Docker (если не очистит) — переустановить Docker Desktop)
#### Посмотреть логи приложения в Docker:
- `docker compose logs -f`
