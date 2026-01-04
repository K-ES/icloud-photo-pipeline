## 2025.12.30 12:18:00

**RU:**  
Создал минимальный Docker-образ на базе `python:3.12-slim`, который выводит
«Здравствуй мир». Разобрался с путями сборки, контекстом Dockerfile и тем,
что базовый образ может не отображаться отдельно. Залогинился в Docker Hub,
протегировал образ с namespace, залил его в registry, удалил локально и
подтвердил воспроизводимость: успешно скачал (`docker pull`) и запустил
образ на чистой системе.

**EN:**  
Created a minimal Docker image based on `python:3.12-slim` that prints
“Hello world”. Understood build context and Dockerfile paths, and that
base images may not appear as standalone images. Logged into Docker Hub,
tagged the image with a namespace, pushed it to the registry, removed it
locally, and verified reproducibility by pulling and running the image
from scratch.


## 2025.12.30 11:03:04

**RU:**  
Изучил Docker Compose: понял, как описывать несколько сервисов в 
одном `docker-compose.yml`, запускать их одной командой и связывать 
контейнеры между собой по именам сервисов.

**EN:**  
Studied Docker Compose: learned how to define multiple services in 
a single `docker-compose.yml`, run them with one command, and connect 
containers via service names.


## 2025.12.30 10:29:04

Первый Docker-образ

RU:
Я установил Docker Desktop без установленного Python на Windows.
Создал Dockerfile и собрал свой первый Docker-образ на базе python-образа.
Понял, что Python и зависимости живут внутри образа.
Контейнер запускается в WSL2 и выполняет процесс, указанный в CMD.
Хостовая система не участвует в выполнении кода.

EN:
I installed Docker Desktop on Windows without local Python.
I created a Dockerfile and built my first Docker image based on a Python image.
I understood that Python and dependencies live inside the image.
The container runs inside WSL2 and executes the process defined in CMD.
The host system is not involved in code execution.


## 2025.12.30 05:38:04

### 🇷🇺 Русский
- Установлен Docker Desktop
- Скачан образ `apache/airflow:2.8.4`
- Понято различие: image / container / volume
- Контейнер запущен одной командой (`airflow standalone`)
- Настроен проброс портов (`HOST:8081 → CONTAINER:8080`)
- Airflow Web UI успешно открыт в браузере
- Логин выполнен через данные из логов контейнера
- Зафиксирована модель: контейнер = процесс, образ = шаблон
- Понято, что Docker убирает ручную установку Python и зависимостей

### 🇬🇧 English
- Docker Desktop installed
- Image `apache/airflow:2.8.4` pulled
- Image / container / volume model understood
- Container started with a single command (`airflow standalone`)
- Port mapping configured (`HOST:8081 → CONTAINER:8080`)
- Airflow Web UI successfully opened
- Login credentials obtained from container logs
- Core model fixed: container = process, image = template
- Docker removes manual Python and dependency setup


## 2025.12.30 04:47:04 
## Docker + WSL storage: итоги эксперимента

### 🇷🇺 Русский

**Ключевая модель**
- Docker Desktop на Windows (WSL2) хранит **ВСЁ состояние** в одном файле:
  `docker_data.vhdx`
- Внутри него:
  - images
  - containers
  - volumes
  - build cache

**Что мы подтвердили на практике**
- Удаление image (`docker rmi`) освобождает место **логически**
- Размер `docker_data.vhdx` **не уменьшается автоматически**
- Физический размер файла:
  - растёт, когда Dockerу нужно больше места
  - **не уменьшается сам**
- `docker system df` — истина про Docker
- размер `docker_data.vhdx` — физика Windows

**Про shrink**
- `Optimize-VHD` — недоступен (нет Hyper-V)
- `wsl --compact` — недоступен в текущем билде
- `--set-sparse`:
  - не уменьшает файл
  - влияет только на будущее поведение
  - сейчас помечен как unsafe
- **Единственный гарантированный способ уменьшить файл**:
  удалить `docker_data.vhdx` при остановленном Docker/WSL  
  → Docker создаёт новый, меньшего размера

**Практический вывод**
- Docker-образы и контейнеры = **кеш**
- Источник истины = **код + Dockerfile + compose**
- Docker можно безопасно «обнулять»

---

### 🇬🇧 English

**Core model**
- Docker Desktop on Windows (WSL2) stores **all state** in a single file:
  `docker_data.vhdx`
- Inside this file:
  - images
  - containers
  - volumes
  - build cache

**What was proven**
- Removing images frees space **logically**, not physically
- `docker_data.vhdx` **does not shrink automatically**
- The file:
  - grows when more space is needed
  - never shrinks by itself
- `docker system df` shows Docker truth
- VHDX size shows Windows disk reality

**About shrinking**
- `Optimize-VHD` unavailable (no Hyper-V)
- `wsl --compact` unavailable in current build
- `--set-sparse`:
  - does not shrink existing file
  - only affects future behavior
  - currently marked unsafe
- **Only guaranteed way to shrink**:
  delete `docker_data.vhdx` with Docker/WSL stopped  
  → Docker recreates a smaller file

**Practical takeaway**
- Docker images & containers = **cache**
- Source of truth = **code + Dockerfile + compose**
- Resetting Docker storage is safe and expected


# 2025.12.29 11:33:52 

1. Основы: Образ ≠ Контейнер. -v маппит папки.
2. Airflow образ: apache/airflow (~800 МБ) - всё готово.
3. Запуск: docker run -p 8080:8080 apache/airflow
4. DAGs локально: -v ./dags:/opt/airflow/dags
5. Веб: localhost:8080, логин: admin/admin
6. Редактируешь DAGs в IDE → Airflow видит сразу.
7. Контейнер изолирован от WSL/системы.
8. Разработка: маппинг папок. Продакшен: свой образ.


1. Basics: Image ≠ Container. -v maps folders.
2. Airflow image: apache/airflow (~800 MB) - everything included.
3. Run: docker run -p 8080:8080 apache/airflow
4. Local DAGs: -v ./dags:/opt/airflow/dags
5. Web UI: localhost:8080, login: admin/admin
6. Edit DAGs in IDE → Airflow sees changes immediately.
7. Container isolated from WSL/system.
8. Dev: volume mapping. Prod: custom image.

# 2025.12.28 09:42:51 

Что я уже изучил и понял про Docker
Docker — это клиент–серверная система (CLI ≠ Engine)
Docker Engine работает в Linux (через WSL), а не в Windows
Команда docker — это пульт управления, а не сам Docker
Docker Desktop UI и CLI делают одно и то же
Контейнер — это обычный Linux-процесс, а не виртуальная машина
Изоляция строится на namespaces и cgroups
Контейнеры маленькие, потому что в них нет ОС и ядра
Image ≠ Container
image — шаблон
container — запущенный экземпляр
Docker image уже содержит установленные Python-библиотеки
pip install выполняется при сборке образа, а не на сервере
Сервер ничего не устанавливает, он только запускает образы
Docker экономит место за счёт слоёв образов
Контейнеры физически лежат в VHDX на Windows, логически — в Linux
В docker-desktop-data не надо лазить руками
Контейнеры видны в WSL как реальные процессы
docker version может сам поднять WSL и сервер
Docker Desktop — это умный автозапуск Linux-сервера
Итог:
Я понял Docker как архитектуру Linux-изоляции, а не как набор команд.


🇬🇧 What I have learned and understood about Docker
Docker is a client–server system (CLI ≠ Engine)
Docker Engine runs inside Linux (via WSL), not Windows
The docker command is a control client, not the engine itself
Docker Desktop UI and CLI do the same thing
A container is just a Linux process, not a virtual machine
Isolation is built using namespaces and cgroups
Containers are small because they do not include an OS or kernel
Image ≠ Container
image = template
container = running instance
A Docker image already contains installed Python libraries
pip install happens at build time, not on the server
The server does not install dependencies, it only runs images
Docker saves disk space using image layers
Containers are physically stored in a Windows VHDX, logically in Linux
You should not manually access docker-desktop-data
Containers appear in WSL as real Linux processes
docker version can automatically start WSL and the engine
Docker Desktop acts as an automatic Linux server launcher
Summary:
I understand Docker as a Linux isolation architecture, not just a set of commands.

# 2025-12-28 06:57:00

Курс https://www.youtube.com/watch?v=_uZQtRyF6Eg

Course https://www.youtube.com/watch?v=_uZQtRyF6Eg