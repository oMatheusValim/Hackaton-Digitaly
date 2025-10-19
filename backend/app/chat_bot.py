import os
import json
from datetime import date, timedelta

# Importa a classe OpenAI
from openai import OpenAI

# A inicialização do cliente busca a chave automaticamente da variável de ambiente
# Garanta que a variável de ambiente OPENAI_API_KEY está configurada
client = OpenAI()

def gerar_resumo_medico(dados_paciente, mensagem_paciente):
    """
    Função principal que orquestra a análise da mensagem do paciente.
    """
    alertas = calcular_alertas_jornada(dados_paciente)
    prompt = montar_prompt_para_llm(dados_paciente, mensagem_paciente, alertas)

    try:
        # Chama a API da OpenAI com a sintaxe atualizada
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente médico especializado em oncologia."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        # Retorna o conteúdo da resposta, que é uma string em formato JSON
        return response.choices[0].message.content
    except Exception as e:
        print(f"Erro ao chamar a API da LLM: {e}")
        return None
        
def montar_prompt_para_llm(dados_paciente, mensagem_paciente, alertas):
    """
    Monta o prompt detalhado que será enviado para a LLM.
    """
    prompt = f"""
    **Contexto do Paciente:**
    - ID: {dados_paciente.get('patient_id')} 
    - Nome: {dados_paciente.get('nome_paciente', 'N/A')}
    - Idade: {dados_paciente.get('idade', 'N/A')}
    - Tipo de Câncer: {dados_paciente.get('tipo_cancer', 'N/A')}
    - Estadiamento: {dados_paciente.get('estadiamento', 'N/A')}
    - Alertas de Atraso na Jornada: {' '.join(alertas) if alertas else 'Nenhum atraso identificado.'}

    **Mensagem do Paciente:**
    "{mensagem_paciente}"

    **Sua Tarefa:**
    Você é um assistente que organiza informações para médicos oncologistas. Analise a mensagem do paciente e os dados de contexto. Sua única saída deve ser um objeto JSON com os seguintes campos:

    1.  `sintomas`: Extraia da mensagem uma lista de todos os sintomas mencionados. Se nenhum for mencionado, retorne uma lista vazia.
    2.  `pontos_relevantes`: Extraia uma lista de outros pontos importantes, como menção a medicamentos, exames, efeitos colaterais ou dúvidas específicas.
    3.  `sugestao_plano_acao`: Com base nos sintomas e pontos relevantes, sugira de 2 a 3 perguntas que o médico pode fazer para investigar melhor o estado do paciente. As perguntas devem ser diretas e focadas.
    4.  `nivel_urgencia`: Classifique a urgência como 'Baixa', 'Média' ou 'Alta', com base na gravidade dos sintomas descritos.

    Responda APENAS com o objeto JSON. Não inclua nenhuma outra palavra ou explicação antes ou depois do JSON.
    """
    return prompt

def calcular_alertas_jornada(dados_paciente):
    """
    Calcula se existe algum atraso na jornada de tratamento do paciente.
    """
    alertas = []
    hoje = date.today()
    limite_dias = timedelta(days=7)

    try:
        data_diagnostico = date.fromisoformat(dados_paciente['diagnostico_data'])
    except (ValueError, TypeError):
        return ["Dados de diagnóstico incompletos."]

    datas_tratamento = []
    for coluna in ['cirurgia_data', 'quimioterapia_inicio', 'radioterapia_inicio']:
        try:
            if dados_paciente[coluna]:
                datas_tratamento.append(date.fromisoformat(dados_paciente[coluna]))
        except (ValueError, TypeError):
            continue

    if not datas_tratamento and (hoje - data_diagnostico > limite_dias):
         alertas.append(f"Atenção: Paciente diagnosticado há mais de {(hoje - data_diagnostico).days} dias sem data de início de tratamento registrada")