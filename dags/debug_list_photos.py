from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from pathlib import Path

DIRS = [
    Path("/mnt/p/Photos/dir1"),
    Path("/mnt/p/Photos/dir2"),
]

def list_files():
    for d in DIRS:
        print(f"DIR: {d}")
        if not d.exists():
            print("  NOT EXISTS")
            continue
        for p in d.iterdir():
            print(" ", p.name)

with DAG(
    dag_id="debug_list_photo_dirs",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
) as dag:
    PythonOperator(
        task_id="list_files",
        python_callable=list_files,
    )
