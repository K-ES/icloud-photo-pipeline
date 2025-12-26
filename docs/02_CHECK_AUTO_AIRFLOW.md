## Проверка Airflow (автозапуск и работоспособность)

Проект использует **Apache Airflow**, запущенный внутри **WSL2 (Ubuntu)** и управляемый через **systemd-сервисы**.  
Для корректной работы предполагается, что Airflow **автоматически запускается при старте WSL** и не зависит от открытого терминала.

Airflow считается корректно настроенным и запущенным, если выполняются следующие условия:

- WSL (Ubuntu) успешно запускается через командную строку Windows  
  (любой вход в WSL инициирует запуск systemd)

- После входа в WSL активны systemd-сервисы Airflow:

      systemctl status airflow-web
      systemctl status airflow-scheduler

  Оба сервиса должны иметь статус:  
  `Active: active (running)`

- Web-интерфейс Airflow доступен по адресу:  
  http://localhost:8080

- Порт 8080 прослушивается внутри WSL:

      ss -ltnp | grep 8080

Пример корректного состояния Airflow:

- airflow-web.service — **running**
- airflow-scheduler.service — **running**
- UI Airflow открывается в браузере без ручного запуска

---

## Check Airflow (Autostart & Health)

This project uses **Apache Airflow** running inside **WSL2 (Ubuntu)** and managed via **systemd services**.  
Airflow is expected to **start automatically when WSL starts** and run independently of any terminal session.

Airflow is considered correctly configured and running if the following conditions are met:

- WSL (Ubuntu) can be successfully launched from the Windows command line  
  (any WSL start triggers systemd initialization)

- After entering WSL, the Airflow systemd services are active:

      systemctl status airflow-web
      systemctl status airflow-scheduler

  Both services should show:  
  `Active: active (running)`

- The Airflow Web UI is accessible at:  
  http://localhost:8080

- Port 8080 is listening inside WSL:

      ss -ltnp | grep 8080

Example of a correct Airflow state:

- airflow-web.service — **running**
- airflow-scheduler.service — **running**
- Airflow UI is available without manual startup
