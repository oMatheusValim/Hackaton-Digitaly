import os
import json
from datetime import date, timedelta
from openai import OpenAI

# Inicializa o cliente (a chave já deve estar no ambiente)
client = OpenAI()

# -----------------------------------------------------------
# Função principal
# -----------------------------------------------------------
def gerar_resumo_medico(dados_paciente, mensagem_paciente):
    """
    Orquestra a análise da mensagem do paciente e gera um resumo estruturado em JSON.
    """
    alertas = calcular_alertas_jornada(dados_paciente)
    prompt = montar_prompt_para_llm(dados_paciente, mensagem_paciente, alertas)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # use modelo mais novo e mais barato
            messages=[
                {"role": "system", "content": "Você é um assistente médico especializado em oncologia."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )

        conteudo = response.choices[0].message.content.strip()

        # Tenta converter o conteúdo em JSON para validação
        try:
            resultado = json.loads(conteudo)
        except json.JSONDecodeError:
            # Se o modelo não retornar JSON puro, tenta extrair manualmente
            resultado = extrair_json(conteudo)

        return resultado

    except Exception as e:
        print(f"Erro ao chamar a API da LLM: {e}")
        return {"erro": str(e)}

# -----------------------------------------------------------
# Prompt de contexto e extração de informações
# -----------------------------------------------------------
# Altere a função montar_prompt_para_llm em chat_bot.py

def montar_prompt_para_llm(dados_paciente, mensagem_paciente, alertas):
    """
    Monta o prompt detalhado que será enviado para a LLM.
    """
    # Pegamos os dados específicos para usar na instrução
    tipo_cancer = dados_paciente.get('tipo_cancer', 'desconhecido')
    estadiamento = dados_paciente.get('estadiamento', 'desconhecido')
    sintoma_principal = mensagem_paciente # Simplificação para o prompt

    prompt = f"""
    **Contexto do Paciente:**
    - ID: {dados_paciente.get('patient_id')} 
    - Tipo de Câncer: {tipo_cancer}
    - Estadiamento: {estadiamento}
    - Outros dados: {dados_paciente}

    **Mensagem do Paciente:**
    "{mensagem_paciente}"

    **Sua Tarefa:**
    Você é um assistente que organiza informações para médicos oncologistas. 
    Analise a mensagem e o contexto e retorne **apenas** um objeto JSON com os seguintes campos:

    {{
        "sintomas": [lista de todos os sintomas mencionados],
        "pontos_relevantes": [lista de outros pontos importantes da mensagem],
        "sugestao_plano_acao": [
            "ANÁLISE CRÍTICA: O paciente tem {tipo_cancer} (estágio {estadiamento}) e relatou '{sintoma_principal}'. 
            Com base nesta conexão específica, formule 2 a 3 perguntas investigativas que um oncologista faria 
            para diferenciar uma emergência de um efeito colateral comum, considerando o diagnóstico principal."
        ],
        "nivel_urgencia": "Baixa" | "Média" | "Alta"
    }}

    Não inclua texto fora do JSON.
    """
    return prompt

# -----------------------------------------------------------
# Cálculo de alertas clínicos
# -----------------------------------------------------------
def calcular_alertas_jornada(dados_paciente):
    """
    Calcula se existe algum atraso na jornada de tratamento do paciente.
    """
    alertas = []
    hoje = date.today()
    limite_dias = timedelta(days=7)

    try:
        data_diagnostico = date.fromisoformat(dados_paciente.get('diagnostico_data', ''))
    except (ValueError, TypeError):
        return ["Dados de diagnóstico incompletos."]

    datas_tratamento = []
    for coluna in ['cirurgia_data', 'quimioterapia_inicio', 'radioterapia_inicio']:
        try:
            if dados_paciente.get(coluna):
                datas_tratamento.append(date.fromisoformat(dados_paciente[coluna]))
        except (ValueError, TypeError):
            continue

    if not datas_tratamento and (hoje - data_diagnostico > limite_dias):

        alertas.append(
            f"Atenção: paciente diagnosticado há {(hoje - data_diagnostico).days} dias sem início de tratamento registrado."
        )

    return alertas

# -----------------------------------------------------------
# Função auxiliar: tenta extrair JSON válido da resposta
# -----------------------------------------------------------
def extrair_json(texto):
    """
    Se o modelo retornar algo como texto + JSON, tenta extrair só o JSON.
    """
    try:
        inicio = texto.index('{')
        fim = texto.rindex('}') + 1
        return json.loads(texto[inicio:fim])
    except Exception:
        return {"texto_bruto": texto}
