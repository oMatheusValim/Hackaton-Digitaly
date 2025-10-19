"use client";

import { useState, useEffect, useMemo } from 'react';

// Dados Fictícios com TIPOS DE CÂNCER adicionados
const DADOS_FAKE_API = [
  { id: "P1", nome_paciente: "Arthur das Neves", tipo_cancer: "Câncer de Colum", alerta_status: "CRITICO", detalhe_atraso: "Diagnóstico -> Estadiamento (+15 dias)" },
  { id: "P2", nome_paciente: "Mariane Novaes", tipo_cancer: "Câncer Colorretal", alerta_status: "CRITICO", detalhe_atraso: "Estadiamento -> Tratamento (+9 dias)" },
  { id: "P3", nome_paciente: "João Miguel da Cunha", tipo_cancer: "Câncer de Mama", alerta_status: "OK", detalhe_atraso: "N/A - Aguardando Exame" },
  { id: "P4", nome_paciente: "Emilly Dias", tipo_cancer: "Câncer de Pulmão", alerta_status: "CRITICO", detalhe_atraso: "Diagnóstico -> Estadiamento (+8 dias)" },
  { id: "P5", nome_paciente: "Marcelo Melo", tipo_cancer: "Câncer de Próstata", alerta_status: "OK", detalhe_atraso: "N/A - Em Tratamento" },
  { id: "P6", nome_paciente: "Lorena Rodrigues", tipo_cancer: "Câncer Colorretal", alerta_status: "CRITICO", detalhe_atraso: "Estadiamento -> Tratamento (+10 dias)" },
  { id: "P7", nome_paciente: "Carlos Alberto", tipo_cancer: "Câncer de Pulmão", alerta_status: "OK", detalhe_atraso: "N/A - Acompanhamento" },
];

export default function DashboardPage() {
  
  // 1. Estados para o array completo de pacientes e os campos de filtro
  const [pacientes, setPacientes] = useState([]);
  const [filtroNome, setFiltroNome] = useState('');
  const [filtroAlerta, setFiltroAlerta] = useState('CRITICO'); // <--- Padrão: Apenas Alerta
  const [filtroCancer, setFiltroCancer] = useState('TODOS');
  
  // Popula os dados na inicialização
  useEffect(() => {
    // Na entrega real, você substituiria esta linha por: fetch('/api/dashboard').then(...)
    setPacientes(DADOS_FAKE_API);
  }, []);

  // Encontra todos os tipos únicos de câncer para popular o dropdown de filtro
  const tiposCancerUnicos = useMemo(() => {
    const tipos = pacientes.map(p => p.tipo_cancer);
    return ['TODOS', ...new Set(tipos)].sort();
  }, [pacientes]);

  // LÓGICA DE FILTRAGEM: Calcula quais pacientes devem ser exibidos
  const pacientesFiltrados = useMemo(() => {
    return pacientes.filter(paciente => {
      
      // 1. Filtragem por Nome (Case-insensitive)
      const nomeMatch = paciente.nome_paciente.toLowerCase().includes(filtroNome.toLowerCase());
      
      // 2. Filtragem por Tipo de Câncer
      const cancerMatch = filtroCancer === 'TODOS' || paciente.tipo_cancer === filtroCancer;

      // 3. Filtragem por Alerta (CRITICO, OK, ou TODOS)
      const alertaMatch = filtroAlerta === 'TODOS' || paciente.alerta_status === filtroAlerta;
      
      return nomeMatch && cancerMatch && alertaMatch;
    });
  }, [pacientes, filtroNome, filtroAlerta, filtroCancer]);


  // 2. ESTRUTURA VISUAL E RENDERIZAÇÃO
  return (
    <main className="dashboard-container">
      <header className="dashboard-header">
        <h1>Dashboard de Indicadores de Alerta</h1>
      </header>
      
      {/* BARRA DE FILTRAGEM (NOVO COMPONENTE) */}
      <section className="filtro-barra">
        
        <div className="filtro-campo">
          <label htmlFor="filtro-nome">Filtrar por Nome:</label>
          <input 
            id="filtro-nome"
            type="text" 
            placeholder="Digite o nome do paciente..."
            value={filtroNome}
            onChange={(e) => setFiltroNome(e.target.value)}
          />
        </div>

        <div className="filtro-campo">
          <label htmlFor="filtro-cancer">Tipo de Câncer:</label>
          <select 
            id="filtro-cancer"
            value={filtroCancer}
            onChange={(e) => setFiltroCancer(e.target.value)}
          >
            {/* Renderiza as opções de câncer dinamicamente */}
            {tiposCancerUnicos.map(tipo => (
              <option key={tipo} value={tipo}>{tipo}</option>
            ))}
          </select>
        </div>

        <div className="filtro-campo">
          <label htmlFor="filtro-alerta">Status do Alerta:</label>
          <select 
            id="filtro-alerta"
            value={filtroAlerta}
            onChange={(e) => setFiltroAlerta(e.target.value)}
          >
            <option value="CRITICO">Ação Crítica (Padrão)</option>
            <option value="OK">OK</option>
            <option value="TODOS">Mostrar Todos</option>
          </select>
        </div>
      </section>
      
      {/* EXIBIÇÃO DOS PACIENTES FILTRADOS */}
      <section className="indicadores-alerta">
        <h2>{pacientesFiltrados.length} Paciente(s) Encontrado(s)</h2>
        
        {pacientesFiltrados.length === 0 ? (
          <p className="nenhum-resultado">Nenhum paciente encontrado com os filtros aplicados.</p>
        ) : (
          pacientesFiltrados.map((paciente) => {
            // LÓGICA DE CLASSE: Se CRITICO, usa a classe vermelha
            const cssClass = paciente.alerta_status === "CRITICO" ? "alerta-critico" : "paciente-ok";

            return (
              <div key={paciente.id} className={`card-paciente-alerta ${cssClass}`}>
                <h3 className="paciente-nome">{paciente.nome_paciente}</h3>
                
                {/* Exibição do Tipo de Câncer */}
                <p className="tipo-cancer">Tipo de Câncer: {paciente.tipo_cancer || 'Não Informado'}</p> 

                <p className="alerta-status">
                  {/* Exibe o status e o detalhe */}
                  {paciente.alerta_status === "CRITICO" ? `⚠️ **AÇÃO CRÍTICA:** ${paciente.detalhe_atraso}` : `Status: ${paciente.detalhe_atraso}`}
                </p>

                <p className="detalhe-alerta">ID: {paciente.id}</p>

                <p><a href={`/chat/medico?id=${paciente.id}`}>Acessar Chat</a></p>
              </div>
            );
          })
        )}
        
      </section>
      
      <p className="navegacao-link">
        <a href="/chat/medico">Acessar Vista do Médico (Exemplo)</a>
      </p>
    </main>
  );
}