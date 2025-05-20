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

4. **Open in browser**

   4.1. **Frontend**  
   - **Locally:** `http://localhost:3001`  
   - **On server:** <https://node100.webte.fei.stuba.sk/PDFToolbox/>

   4.2. **Backend (API)**  
   - **Locally:**  
     - `http://localhost:8000/api`  
     - `http://localhost:8000/api/docs` — for documentation  
   - **On server:**  
     - <https://node100.webte.fei.stuba.sk/PDFToolbox/api>  
     - <https://node100.webte.fei.stuba.sk/PDFToolbox/api/docs> — for documentation

   4.3. **MongoDB**  
   - URI: `mongodb://mongodb:27017`

6. **Stop the application:**

    Press `Ctrl + C` or run the command:

    ```bash
    docker compose down
    ```

7. **Restart the application:**

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
