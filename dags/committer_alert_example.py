"""
Astronaut-style “fail demo” DAG
===============================

This DAG intentionally raises a SQL error every run so you can:

* test alerting/notification systems (e.g., Astro Platform alerts that e-mail
  the most-recent committer);
* verify that the Airflow scheduler surfaces parse/run-time errors correctly;

How it works
------------
1. A single ``SQLExecuteQueryOperator`` queries a non-existent table.
2. The query fails instantly, marking the whole DAG run as *failed*.
3. Any Deployment-level ``DAG_FAILURE`` alert fires (great for demos).

Related tutorials
-----------------
* “Write your first DAG” → https://www.astronomer.io/docs/learn/get-started-with-airflow
Test #1

"""

from __future__ import annotations

from datetime import timedelta

from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.utils.dates import days_ago

# ---------------------------------------------------------------------------
# Default DAG arguments applied to *every* task unless overridden.
# ---------------------------------------------------------------------------
default_args = {
    "owner": "demo",
    "retries": 0,
    "execution_timeout": timedelta(minutes=5),
}

# ---------------------------------------------------------------------------
# DAG definition
# ---------------------------------------------------------------------------
with DAG(
    dag_id="fail_demo_dag",
    description="Intentionally fails a SQL query to demo alerting / failure handling",
    start_date=days_ago(1),
    schedule_interval="@daily",
    catchup=False,
    default_args=default_args,
    tags=["demo", "alert", "failure"],
) as dag:

    # Task: run a bogus SQL query so the DAG fails every run
    break_me = SQLExecuteQueryOperator(
        task_id="break_me",
        sql="SELECT * FROM table_that_does_not_exist",
    )

    # No downstream dependencies – the DAG stops right here on failure