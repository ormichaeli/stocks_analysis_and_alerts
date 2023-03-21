import sys
from airflow.models import DAG
from datetime import datetime, time, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator

dir = '/tmp/pycharm_project_598'

sys.path.insert(0, dir)

# retries: give the dag a maximum of two retries in case of failure
# retry_delay: tell the DAG to wait 1 minute before retrying
dag = DAG(
    dag_id="run_send_emails",
    default_args={
        "owner": 'Airflow'
    },
    start_date= datetime(2023, 3, 18),
    schedule_interval='58 8 * * 1-5',        # At 08:58 AM, Monday through Friday
    tags=['stocks_analysis_and_alerts_final_project']
)

run_stream_send_emails = BashOperator(
    task_id='run_stream_send_emails',
    bash_command= f"python {dir}/streaming/stream_send_emails.py",
    dag=dag,
)

dummy_task = DummyOperator(task_id='dummy_task', dag=dag)

dummy_task >> run_stream_send_emails

if __name__ == "__main__":
    dag.cli()