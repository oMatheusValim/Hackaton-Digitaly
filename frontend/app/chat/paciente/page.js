"use client";

import { useState, useEffect, useRef } from 'react';

// Dados Fictícios Iniciais para o Histórico (Simulação da API)
const HISTORICO_INICIAL_FAKE = [
  // Mensagem de exemplo para iniciar o chat
  { remetente: 'medico', mensagem: 'Dr. Souza: Olá, como você está se sentindo hoje? Recebi as notas da sua última consulta.' },
  { remetente: 'paciente', mensagem: 'Você: Dr., estou com uma dor de cabeça persistente desde ontem e um pouco de enjoo.' },
];

export default function ChatPacientePage() {
  
  // 1. Estados para o chat
  const [historico, setHistorico] = useState(HISTORICO_INICIAL_FAKE);
  const [inputMensagem, setInputMensagem] = useState('');
  
  // Ref para manter a rolagem do chat sempre no final
  const chatEndRef = useRef(null);

  // Efeito para rolar para o final do chat sempre que uma nova mensagem chega
  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [historico]);
  
  // 2. Função de Envio de Mensagem
  const handleEnviarMensagem = (e) => {
    // Evita o recarregamento da página se for um submit de formulário
    if (e) e.preventDefault(); 
    
    const mensagemTrimada = inputMensagem.trim();
    if (!mensagemTrimada) return; // Não envia se a mensagem estiver vazia

    // Adiciona a nova mensagem do paciente ao histórico
    const novaMensagem = { 
      remetente: 'paciente', 
      mensagem: `Você: ${mensagemTrimada}` 
    };
    
    setHistorico(prev => [...prev, novaMensagem]); // Adiciona ao fim do array
    setInputMensagem(''); // Limpa o input
    
    // Simulação da resposta do Agente (LLM/Backend) após um breve delay
    simularRespostaBackend();
  };
  
  // 3. Simulação de Resposta do Backend/Agente
  const simularRespostaBackend = () => {
    setTimeout(() => {
      const respostaAutomatica = {
        remetente: 'medico', 
        mensagem: 'Dr. Souza (Agente): Obrigado pela informação. Vou notificar o Dr. Souza sobre o seu relato. Por favor, aguarde o retorno ou cheque seu status no app.'
      };
      // Adiciona a resposta do backend após 2 segundos
      setHistorico(prev => [...prev, respostaAutomatica]);
    }, 2000); 
  };


  return (
    <div className="chat-view-container-paciente">
      
      <h1 className="titulo-chat">
        Chat com Dr. Rodrigo Souza (Seu Médico)
      </h1>

      <section className="interface-chat-paciente">
        
        {/* Histórico de Mensagens - RENDERIZAÇÃO DINÂMICA */}
        <div className="historico-mensagens-paciente">
          {historico.map((msg, index) => {
            
            // LÓGICA DE ALINHAMENTO CORRIGIDA:
            // 1. VERIFICAÇÃO: Se o remetente é o 'paciente', ele é o usuário logado (isUser = true)
            const isUser = msg.remetente === 'paciente'; 
              
            // 2. CONSTRUÇÃO DA CLASSE: Adiciona 'user-message' se for o usuário logado
            // A classe 'user-message' no CSS alinha à direita.
            const classes = `mensagem ${msg.remetente} ${isUser ? 'user-message' : ''}`;
            
            return (
              <div 
                key={index} 
                className={classes} // Aplica a classe montada
              >
                {msg.mensagem}
              </div>
            );
          })}
          <div ref={chatEndRef} />
        </div>
        
        {/* Área de Input (Formulário para envio com Enter) */}
        <form className="input-mensagem-area-paciente" onSubmit={handleEnviarMensagem}>
          <input 
            type="text" 
            placeholder="digite aqui" 
            className="input-chat" 
            value={inputMensagem} // Controlado pelo estado
            onChange={(e) => setInputMensagem(e.target.value)} // Atualiza o estado
          />
          <button 
            type="submit" 
            className="enviar-btn"
          >
            &gt;
          </button>
        </form>
        
      </section>
      
      <p className="navegacao-link">
        <a href="/dashboard">Voltar para o Dashboard</a>
      </p>
    </div>
  );
}
