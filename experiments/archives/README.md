# Archive extraction experiments

## Purpose
Исследование и реализация разархивации архивов (фото / видео) через Python  
с прицелом на дальнейшее использование в Airflow DAG.

## Scope
- работа с локальными архивами
- без iCloud API
- без обработки медиа
- только extract → filesystem

## Supported formats
- zip (обязательно)
- 7z, rar (позже, опционально)

## Input
- путь к архиву
- целевой каталог для распаковки

## Output
- распакованные файлы
- сохранённая структура каталогов

## Requirements
- Python 3.10+
- стандартная библиотека (zipfile) на первом этапе

## Design notes
- код идемпотентный
- без Airflow-зависимостей
- готов к оборачиванию в PythonOperator / TaskFlow

## Files
- `unzip_zip.py` — экспериментальная логика распаковки zip
- `__init__.py` — для импорта как модуля

## Next steps
- обработка ошибок
- dry-run режим
- подготовка интерфейса под Airflow task
