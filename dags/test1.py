from airflow.sdk.definitions.asset import Asset
from airflow.decorators import dag, task
from pendulum import datetime
import requests


# Define the basic parameters of the DAG, like schedule and start_date
@dag(
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args={"owner": "Astro", "retries": 3},
    tags=["example"],
)
def test1():
    @task()
    def get_astronauts():
        print("this code version 1")
    
    get_astronauts()

test1()