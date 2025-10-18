# Hackathon-Digitaly - Plataforma de Suporte Oncológico

## 🎯 Objetivo

O objetivo deste projeto é o desenvolvimento de uma plataforma médica focada em otimizar a jornada de tratamento de pacientes oncológicos. A solução visa fornecer ao corpo médico ferramentas inteligentes para acompanhamento, triagem e tomada de decisão, utilizando um Large Language Model (LLM) para extrair e sumarizar informações cruciais.

## 📝 Descrição do Projeto

A plataforma é composta por módulos que facilitam a interação e o monitoramento de pacientes com câncer. O escopo do MVP (Minimum Viable Product) inclui duas funcionalidades centrais: um **Agente de Suporte ao Médico** (via chat) e um **Dashboard de Alertas**, ambos construídos sobre uma base de dados fictícia de pacientes.

A ideia central é que, durante a interação com o paciente, o médico tenha acesso a um resumo automático e inteligente, destacando sintomas, pontos de atenção e possíveis ações, agilizando o atendimento e aumentando a precisão do cuidado.

## ✨ Funcionalidades (MVP)

### 1. Agente de Suporte via Chat

  - **Interface de Chat**: Uma tela de chat em tempo real para comunicação entre médico e paciente.
  - **Resumo Automático para o Médico**: Durante a conversa, a LLM gera e exibe um resumo ao lado do chat, contendo:
      - **Identificação do Paciente**: Informações básicas extraídas da base de dados.
      - **Principais Sintomas Mencionados**: Uma lista com os sintomas que o paciente descreve na conversa.
      - **Pontos Relevantes**: Outras informações importantes capturadas, como menção a exames, medicamentos ou efeitos colaterais.
      - **Sugestão de Plano de Ação**: Recomendações de perguntas e próximos passos para o médico.
  - **Sistema de Alertas**: Identificação automática de atrasos na jornada do paciente, com um alerta sendo gerado se o tempo entre as etapas exceder 7 dias:
      - `Diagnóstico -> Estadiamento` 
      - `Estadiamento -> Tratamento`

### 2. Dashboard de Indicadores

  - **Visualização de Alertas**: Um painel que exibe de forma clara os pacientes que possuem alertas de atraso em suas jornadas de tratamento, permitindo uma ação rápida da equipe médica.
  - **Critério de Atraso**: Utiliza a mesma regra de 7 dias definida para o módulo do chat.

### ⭐ Funcionalidades Bônus

  - **Nível de Urgência**: A IA classifica a criticidade da mensagem do paciente (Baixa, Média, Alta).

## 🛠️ Ferramentas e Tecnologias

  - **Backend**: Python 
  - **Frontend**: Next.js
  - **Banco de Dados**: MongoDB 
  - **Inteligência Artificial**: Modelo GPT da OpenAI

## 🏆 Criadores

  - [Matheus Valim](https://github.com/oMatheusValim)
  - [Bruno Zuffo](https://github.com/BrunoZuffo)
  - [Arthur Albuquerque](https://github.com/Arthas01)