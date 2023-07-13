import sys
import os

from datetime import datetime, timedelta
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator
from Utils.utils import update_schedulers_config

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'hourly_trigger',
    default_args=default_args,
    schedule_interval='@hourly',
)

def reset_hourly_configurations():
    update_schedulers_config('total_number_of_api_calls_to_linkedin',  0)

reset_task = PythonOperator(
    task_id='reset_hourly_configurations',
    python_callable=reset_hourly_configurations,
    dag=dag,
)

email_address = Variable.get('email_notification')
email_success_task = EmailOperator(
    task_id='send_success_email',
    to=email_address,
    subject='SUCCESS: Reset Linkedin Api Calls',
    html_content='The hourly task completed successfully.',
    dag=dag,
)

email_failure_task = EmailOperator(
    task_id='send_failure_email',
    to=email_address,
    subject='FAILURE: Reset Linkedin Api Calls',
    html_content='The hourly task failed to complete.',
    dag=dag,
)

reset_task >> email_success_task
reset_task >> email_failure_task
    