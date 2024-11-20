import random
from datetime import datetime, timedelta

def generate_registration_data():
    # Cursos possíveis e regras relacionadas
    cursos = ["Mecânica Industrial", "Informática para Web", "Edificações", "Refrigeração", "Administração"]
    turnos = ["Manhã", "Tarde", "Noite"]
    pagamentos = ["Crédito", "Débito", "Dinheiro", "Pix", "Boleto à Vista", "Boleto Carnê", "Outros"]
    sexos = ["Masculino", "Feminino", "Não Declarado"]
    responsavel_financeiro_opcoes = ["Sim", "Não"]
    
    curso_nome = random.choice(cursos)
    curso_turno = random.choice(turnos)

    # Definir duração do curso
    if curso_nome in ["Mecânica Industrial", "Edificações", "Refrigeração"]:
        curso_duracao = 4 if curso_turno in ["Manhã", "Tarde"] else 5
    else:
        curso_duracao = 3 if curso_turno in ["Manhã", "Tarde"] else 4

    # Definir data de início do curso
    data_base = datetime(2024, 2, 1)  # Data base de referência para o exemplo
    if curso_turno == "Noite":
        curso_inicio = data_base
    elif curso_nome in ["Mecânica Industrial", "Edificações", "Informática para Web"]:
        curso_inicio = data_base + timedelta(weeks=1)
    else:
        curso_inicio = data_base + timedelta(weeks=2)

    # Definir idade do aluno
    prob_idade = random.uniform(0, 1)
    if prob_idade < 0.7:  # Concentração maior entre 18 e 25 anos
        idade = random.randint(18, 25)
    else:
        idade = random.randint(14, 99)
    
    # Definir responsável financeiro
    if idade > 21:
        responsavel_financeiro = "Sim"
    else:
        responsavel_financeiro = random.choice(responsavel_financeiro_opcoes)

    # Definir data de matrícula
    matricula_inicio = curso_inicio - timedelta(weeks=16)  # Até 4 meses antes
    matricula_fim = curso_inicio + timedelta(weeks=2)      # Até 2 semanas após
    prob_matricula = random.uniform(0, 1)
    if prob_matricula < 0.8:  # Maior concentração nos últimos 30 dias e 5 dias após o início
        matricula_inicio_reducida = curso_inicio - timedelta(days=30)
        matricula_fim_reducida = curso_inicio + timedelta(days=5)
        dt_matricula = matricula_inicio_reducida + timedelta(
            days=random.randint(0, (matricula_fim_reducida - matricula_inicio_reducida).days)
        )
    else:
        dt_matricula = matricula_inicio + timedelta(
            days=random.randint(0, (matricula_fim - matricula_inicio).days)
        )

    return {
        'id_matricula': str(random.randint(10000, 99999)),  # Unique ID for the registration
        'ds_curso_nome': curso_nome,
        'ds_curso_turno': curso_turno,
        'ds_curso_duracao': curso_duracao,
        'ds_curso_inicio': curso_inicio.strftime('%Y-%m-%d'),
        'ds_aluno_idade': idade,
        'ds_aluno_sexo': random.choice(sexos),
        'ds_aluno_responsavel_financeiro': responsavel_financeiro,
        'ds_matricula_pagamento': random.choice(pagamentos),
        'dt_matricula': dt_matricula.strftime('%Y-%m-%d')
    }

if __name__ == "__main__":
    # Código a ser executado se o arquivo for chamado diretamente
    for _ in range(5):  # Exemplo de execução direta
        print(generate_registration_data())