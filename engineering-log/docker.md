2025.12.28 09:42:51 
🇷🇺 Что я уже изучил и понял про Docker
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
2025-12-28 06:57:00 - Курс https://www.youtube.com/watch?v=_uZQtRyF6Eg
                      Course https://www.youtube.com/watch?v=_uZQtRyF6Eg