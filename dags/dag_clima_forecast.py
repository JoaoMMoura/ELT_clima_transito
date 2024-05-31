from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
import snowflake.connector
from datetime import datetime
import pytz

def get_base_clima_proximos_dias(cidades, pais, dias, appid):
    dados_clima_forecast = []
    for cidade in cidades:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={cidade},{pais}&cnt={dias}&appid={appid}&units=metric&lang=pt_br"
        resposta = requests.get(url)
        dados = resposta.json()
        if resposta.status_code == 200:
            for item in dados["list"]:
                dados_clima_forecast.append({
                    "temp": item["main"]["temp"],
                    "temp_min": item["main"]["temp_min"],
                    "temp_max": item["main"]["temp_max"],
                    "humidity": item["main"]["humidity"],
                    "weather_description": item["weather"][0]["description"],
                    "dt_txt": item["dt_txt"],
                    "local": f'{cidade}'
                })
        else:
            return resposta.status_code
    return dados_clima_forecast

def inserir_dados_snowflake(table_name, data):
    # Configurações de conexão
    conn = snowflake.connector.connect(
    )

    # Criação de um cursor
    cursor = conn.cursor()

    # Dicionário de consultas SQL
    sql_queries = {
        'clima': """
            INSERT INTO clima (temp, feels_like, temp_min, temp_max, 
           humidity, date_insertion, local)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        'transito': """
            INSERT INTO transito (origem, destino, distancia, duracao, date_insertion)
            VALUES (%s, %s, %s, %s, %s)
        """,
        'clima_forecast': """
            INSERT INTO clima_forecast (temp, temp_min, temp_max, humidity, 
            descricao, date_forecast, local)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
    }

    # Inserção dos dados na tabela
    try:
        date_tz = pytz.timezone('America/Sao_Paulo')
        query = sql_queries.get(table_name)
        if query:
            if table_name == 'clima':
                cursor.execute("TRUNCATE TABLE clima")
                for item in data:
                    cursor.execute(query, (item['main']['temp'], item['main']['feels_like'],
                                        item['main']['temp_min'], item['main']['temp_max'],
                                        item['main']['humidity'], datetime.now(date_tz), item['name']))
                conn.commit()
            elif table_name == 'transito':
                cursor.execute("TRUNCATE TABLE transito")
                for item in data:
                    cursor.execute(query, (item['origem'], item['destino'], item['distancia'], item['duracao'],
                                           datetime.now(date_tz)))
                    conn.commit()
            elif table_name == 'clima_forecast':
                cursor.execute("TRUNCATE TABLE clima_forecast")
                for item in data:
                    cursor.execute(query, (
                        item['temp'], item['temp_min'], item['temp_max'], item['humidity'], item['weather_description'],
                        item['dt_txt'], item['local']))
                    conn.commit()
            print("Dados inseridos com sucesso!")
        else:
            print("Tabela não encontrada.")
    except snowflake.connector.errors.ProgrammingError as e:
        print("Erro ao inserir dados:", e)
    finally:
        # Fechar conexão
        cursor.close()
        conn.close()

# Configuração padrão da DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Criação da DAG
with DAG('elt_clima_forecast',
         default_args=default_args,
         description='DAG para coletar dados de clima e trânsito e inserir no Snowflake',
         schedule_interval='0 */3 * * *',
         catchup=False,
         max_active_runs=1) as dag:

    def tarefa_clima_forecast():
        cidades = ['Formosa', 'Brasilia', 'Planaltina', 'Sobradinho']
        pais = 'BR'
        dias = 40
        appid = ''
        dados_clima_forecast = get_base_clima_proximos_dias(cidades, pais, dias, appid)
        inserir_dados_snowflake('clima_forecast', dados_clima_forecast)


    tarefa_transito = PythonOperator(
        task_id='tarefa_clima_forecast',
        python_callable=tarefa_clima_forecast,
        dag=dag
    )


    # Define a ordem de execução das tarefas
    [tarefa_clima_forecast]
