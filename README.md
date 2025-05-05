# PDFToolbox

## Начало работы

### Необходимые компоненты
- [Git](https://git-scm.com/downloads)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Системные требования
- Свободное место: 5–8 ГБ
- Оперативная память: минимум 2 ГБ

## Установка и запуск

1. **Клонировать репозиторий:**

    ```bash
    git clone https://github.com/OlegQm/PDFToolbox.git
    ```

2. **Перейти в папку проекта:**

    ```bash
    cd PDFToolbox
    ```

3. **Запустить контейнеры:**

    ```bash
    docker compose up --build
    ```

4. **Открыть в браузере:**

    4.1. **Фронтенд**  
    &nbsp;&nbsp;&nbsp;&nbsp;• Локально: `http://localhost:3001`  
    &nbsp;&nbsp;&nbsp;&nbsp;• На сервере: `https://node100.webte.fei.stuba.sk/PDFToolbox/`

    4.2. **Бэкенд (API)**  
    &nbsp;&nbsp;&nbsp;&nbsp;• Локально:  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`http://localhost:8000/api`  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`http://localhost:8000/api/docs` — если нужна документация  
    &nbsp;&nbsp;&nbsp;&nbsp;• На сервере:  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`https://node100.webte.fei.stuba.sk/PDFToolbox/api`  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`https://node100.webte.fei.stuba.sk/PDFToolbox/api/docs` — если нужна документация

    4.3. **MongoDB**  
    &nbsp;&nbsp;&nbsp;&nbsp;• URI: `mongodb://mongodb:27017`

5. **Остановить приложение:**

    Нажмите `Ctrl + C` или выполните команду:

    ```bash
    docker compose down
    ```

6. **Перезапустить приложение:**

    ```bash
    docker compose down && docker compose up --build
    ```

## Полезные команды
#### Очистить файлы Docker-а
- `docker compose down --volumes --remove-orphans`
- `docker system prune -a --volumes -f`
- При проблемах с Docker (если не очистит) — переустановить Docker Desktop
#### Посмотреть логи приложения в Docker:
- `docker compose logs -f`
