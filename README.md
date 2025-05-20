# PDFToolbox

## Getting Started

### Required Components
- [Git](https://git-scm.com/downloads)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### System Requirements
- Free space: 5 GB
- RAM: at least 2 GB

## Installation and Launch

1. **Clone the repository:**

    ```bash
    git clone https://github.com/OlegQm/PDFToolbox.git
    ```

2. **Go to the project folder:**

    ```bash
    cd PDFToolbox
    ```

3. **Start the containers:**

    ```bash
    docker compose up --build
    ```

4. **Open in browser:**

    4.1. **Frontend**
    &nbsp;&nbsp;&nbsp;&nbsp;• Locally: `http://localhost:3001`
    &nbsp;&nbsp;&nbsp;&nbsp;• On server: `https://node100.webte.fei.stuba.sk/PDFToolbox/`

    4.2. **Backend (API)**
    &nbsp;&nbsp;&nbsp;&nbsp;• Locally:
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`http://localhost:8000/api`  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`http://localhost:8000/api/docs` — for documentation
    &nbsp;&nbsp;&nbsp;&nbsp;• On server:
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`https://node100.webte.fei.stuba.sk/PDFToolbox/api`
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`https://node100.webte.fei.stuba.sk/PDFToolbox/api/docs` — for documentation

    4.3. **MongoDB**  
    &nbsp;&nbsp;&nbsp;&nbsp;• URI: `mongodb://mongodb:27017`

5. **Stop the application:**

    Press `Ctrl + C` or run the command:

    ```bash
    docker compose down
    ```

6. **Restart the application:**

    ```bash
    docker compose down && docker compose up --build
    ```

## Useful Commands
#### Clean Docker files
- `docker compose down --volumes --remove-orphans`
- `docker system prune -a --volumes -f`
- If you have issues with Docker (if not cleaned) — reinstall Docker Desktop
#### View application logs in Docker:
- `docker compose logs -f`
