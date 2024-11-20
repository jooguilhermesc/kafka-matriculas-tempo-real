import streamlit as st
from kafka import KafkaConsumer
import pandas as pd
import json
import time
from datetime import datetime
import matplotlib.pyplot as plt

# Função para consumir mensagens do Kafka
def consume_kafka_messages():
    consumer = KafkaConsumer(
        'registration_topic',  # O tópico Kafka
        api_version=(3, 8, 0),
        bootstrap_servers='kafka:9092',  # Servidor Kafka
        auto_offset_reset='earliest',  # Lê desde o início, se necessário
        enable_auto_commit=True,
        group_id='registration_consumer_group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    return consumer

def fetch_data_from_kafka(consumer):
    
    messages = consumer.poll(timeout_ms=10000)  # Poll for messages for 1 second
    data = []

    for topic_partition, records in messages.items():
        for record in records:
            data.append(record.value)

    return data

# Função para calcular o perfil mais comum
def get_common_profile(df):
    profile = {
        "Sexo": df['ds_aluno_sexo'].mode()[0],
        "Idade": df['ds_aluno_idade'].mode()[0],
        "Turno": df['ds_curso_turno'].mode()[0],
        "Responsável Financeiro": df['ds_aluno_responsavel_financeiro'].mode()[0],
        "Tipo de Pagamento": df['ds_matricula_pagamento'].mode()[0],
        "Curso Mais Procurado": df['ds_curso_nome'].mode()[0],
    }
    return profile

# Configuração do Streamlit
st.set_page_config(page_title="Matrículas - Tempo Real", layout="wide")
st.title("Dashboard de Matrículas")

# Loop de atualização automática
placeholder = st.empty()

while True:
    with placeholder.container():
        try:
            # Consome as mensagens do Kafka
            kafka_consumer = consume_kafka_messages()
            kafka_data = fetch_data_from_kafka(kafka_consumer)
            df = pd.DataFrame(kafka_data)
            if not df.empty:
                col1, col2 = st.columns(2)

                # Total de matrículas
                total_matriculas = len(df['id_matricula'].unique())
                col1.metric(label="Total de Matrículas", value=total_matriculas)

                # Última atualização
                col2.markdown(f"**Última atualização:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                col1, col2, col3 = st.columns(3)

                # Gráfico de matrículas por curso
                col1.markdown("### Matrículas por Curso")
                matriculas_por_curso = df['ds_curso_nome'].value_counts()
                col1.bar_chart(matriculas_por_curso, use_container_width=True, height=400)
                
                # Gráfico de matrículas por tipo de pagamento
                col2.markdown("### Matrículas por Tipo de Pagamento")
                matriculas_por_pagamento = df['ds_matricula_pagamento'].value_counts()
                col2.bar_chart(matriculas_por_pagamento, use_container_width=True, height=400)
                
                # Gráfico de rosca para matrículas por turno
                col3.markdown("### Percentual de Matrículas por Turno")
                matriculas_por_turno = df['ds_curso_turno'].value_counts(normalize=True) * 100
                fig, ax = plt.subplots(figsize=(8, 8))
                matriculas_por_turno.plot.pie(autopct='%1.1f%%', ax=ax, legend=False)
                ax.set_title("Percentual de Matrículas por Turno")
                col3.pyplot(fig)
                
                # Perfil mais comum
                profile = get_common_profile(df)
                st.markdown("### Perfil Mais Comum")
                st.json(profile)

                # Tabela com os dados consumidos
                st.markdown("### Matrículas realizadas")
                st.dataframe(df)
                
            else:
                st.warning("Nenhum dado foi consumido do Kafka.")
        except Exception as e:
            st.error(f"Erro ao consumir dados: {e}")
    
    time.sleep(10)  # Atualiza a cada 10 segundos
