"use client";

import { useState, useEffect, useRef } from 'react';

// 1. DADOS INICIAIS FAKE (Simulação do que viria da API)
const HISTORICO_INICIAL_FAKE = [
  { remetente: 'medico', mensagem: 'Dr. Souza: Olá, Arthur. Estou aqui para analisar o seu caso. Qual sua principal preocupação hoje?' },
  { remetente: 'paciente', mensagem: 'Arthur: Olá, Dr. Eu estou com muita dor na região lombar ultimamente. Sinto também um cansaço muito forte.' },
  { remetente: 'paciente', mensagem: 'Arthur: E percebi que estou com pouca vontade de comer nas últimas semanas.' },
];

// 2. RESUMO LLM INICIAL FAKE
const RESUMO_INICIAL_FAKE = {
  paciente_id: "P-8100",
  nome: "Arthur das Neves",
  idade: 26,
  tipo_cancer: "Câncer de mama (Estadiamento IIA)",
  alerta: {
    status: "CRITICO",
    detalhe: "Atraso em Estadiamento -> Tratamento (+9 dias)",
    // ESTADO INICIAL DA LLM
    acao_sugerida: "Aguardando novas informações do paciente para análise da LLM." 
  },
  // ESTADO INICIAL DA LLM
  sintomas: ["Nenhum sintoma relevante detectado ainda."], 
  observacoes: "Paciente tem histórico de tabagismo. Alerta de atraso ativo. (Pontos Iniciais)."
};

// 3. RESUMO LLM ATUALIZADO (O que viria após a análise da 6ª mensagem)
const RESUMO_ATUALIZADO_FAKE = {
  ...RESUMO_INICIAL_FAKE, // Mantém dados de identificação
  alerta: {
    ...RESUMO_INICIAL_FAKE.alerta,
    acao_sugerida: "Verificar exames recentes. Paciente relata dor lombar (meta de rastreamento) e forte fadiga. Sugerir reagendamento urgente." // ATUALIZADO
  },
  sintomas: [ // ATUALIZADO
    "Dor na região lombar (Ponto Focal)",
    "Fadiga e cansaço constante",
    "Perda de apetite"
  ], 
  observacoes: "Paciente mencionou dor lombar (que pode ser metástase). LLM sugere risco alto. Histórico de tabagismo. Exames devem ser priorizados." // ATUALIZADO
};


export default function ChatMedicoPage() {
  
  const [historico, setHistorico] = useState(HISTORICO_INICIAL_FAKE);
  const [resumoData, setResumoData] = useState(RESUMO_INICIAL_FAKE);
  const [inputMensagem, setInputMensagem] = useState('');
  
  const chatEndRef = useRef(null);
  
  // Rola para o final do chat
  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [historico]);
  
  // 4. Função de Envio de Mensagem (Médico)
  const handleEnviarMensagem = (e) => {
    if (e) e.preventDefault(); 
    
    const mensagemTrimada = inputMensagem.trim();
    if (!mensagemTrimada) return;

    // Adiciona a mensagem do médico
    const novaMensagem = { 
      remetente: 'medico', 
      mensagem: `Dr. Souza: ${mensagemTrimada}` 
    };
    
    setHistorico(prev => [...prev, novaMensagem]);
    setInputMensagem('');
    
    // Na vida real, esta seria a API do backend salvando a mensagem.
  };

  // 5. Função para SIMULAR a Análise da LLM
  const simularAnaliseLLM = () => {
    alert("Simulando que o Paciente enviou 6 mensagens. O Backend está reanalisando a conversa...");
    
    // Simula a latência de análise da LLM (3 segundos)
    setTimeout(() => {
      // ATUALIZA O RESUMO com os dados "analisados"
      setResumoData(RESUMO_ATUALIZADO_FAKE);
    }, 3000); 
  };
  
  // 6. Estrutura Visual do Resumo
  const alertaClass = resumoData.alerta.status === "CRITICO" ? "alerta-critico" : "";

  return (
    <div className="chat-view-container">
      <h1 className="titulo-chat">
        Agente de Suporte | Paciente: {resumoData.nome} (ID: {resumoData.paciente_id})
      </h1>

      <div className="main-chat-layout"> 
        
        {/* COLUNA ESQUERDA: RESUMO AUTOMÁTICO - PRONTO PARA LLM */}
        <aside className="resumo-paciente-panel">
          <h2>RESUMO AUTOMÁTICO (LLM-READY)</h2>
          
          <div className="resumo-card identificacao-card">
            <h3>Identificação do paciente</h3>
            <p><strong>Nome:</strong> {resumoData.nome}</p>
            <p><strong>Condição:</strong> {resumoData.tipo_cancer}</p>
          </div>

          <div className={`resumo-card alerta-card ${alertaClass}`}>
            <h3>Alertas</h3>
            <p>{resumoData.alerta.detalhe}</p>
          </div>

          {/* SINTOMAS - Atualizado pela LLM */}
          <div className="resumo-card sintomas-card">
            <h3>Principais Sintomas</h3>
            <ul className="lista_sintomas">
              {resumoData.sintomas.map((sintoma, index) => (
                <li key={index}>{sintoma}</li>
              ))}
            </ul>
          </div>
          
          {/* OBSERVAÇÕES / PONTOS RELEVANTES - Atualizado pela LLM */}
          <div className="resumo-card observacoes-card">
            <h3>Observações / Pontos Relevantes</h3>
            <p>{resumoData.observacoes}</p>
          </div>
          
          {/* SUGESTÃO PLANO DE AÇÃO - Atualizado pela LLM */}
          <div className="resumo-card plano-acao-card">
            <h3>Sugestão plano de ação</h3>
            <p>{resumoData.alerta.acao_sugerida}</p>
          </div>
          
          <button onClick={simularAnaliseLLM} style={{ width: '100%', padding: '10px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', marginTop: '10px' }}>
            [Simular Análise LLM - Após 6 mensagens]
          </button>

        </aside>

        {/* COLUNA DIREITA: Interface do Chat Dinâmica */}
        <section className="interface-chat">
          <div className="historico-mensagens">
            {historico.map((msg, index) => {
              
              // LÓGICA DE ALINHAMENTO CORRETA
              // 1. VERIFICAÇÃO: Se o remetente é o médico, ele é o usuário logado (isUser = true)
              const isUser = msg.remetente === 'medico'; 
              
              // 2. CONSTRUÇÃO DA CLASSE: Adiciona 'user-message' se for o usuário logado
              const classes = `mensagem ${msg.remetente} ${isUser ? 'user-message' : ''}`;

              return (
                <div 
                  key={index} 
                  className={classes} // Usa as classes montadas
                >
                  {msg.mensagem}
                </div>
              );
            })}
            <div ref={chatEndRef} />
          </div>
          
          <form className="input-mensagem-area" onSubmit={handleEnviarMensagem}>
            <input 
              type="text" 
              placeholder="Digite sua resposta aqui..." 
              className="input-chat" 
              value={inputMensagem}
              onChange={(e) => setInputMensagem(e.target.value)}
            />
            <button 
              type="submit" 
              className="enviar-btn"
            >
              &gt;
            </button>
          </form>
        </section>
        
      </div>
    </div>
  );
}