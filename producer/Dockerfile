# Imagem Base
FROM python:3.9

# Pasta de trabalho
WORKDIR /app

# Copiando script
COPY producer/producer.py /app

# Copiando script
COPY producer/generate_data.py /app

# Instalando dependências
RUN pip install kafka-python faker

# Rodando script
CMD ["python", "producer.py"]