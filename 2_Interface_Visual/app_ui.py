import streamlit as st
import requests
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_URL = "http://localhost:8000"

def check_api_health() -> bool:
    try:
        response = requests.get(f"{API_URL}/health", timeout=3)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# CONFIGURAÇÃO DE RENDERIZAÇÃO DA PÁGINA
st.set_page_config(
    page_title="NLP Support Suite | Enterprise IA",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🤖 Plataforma NLP de Triagem de Suporte")
st.caption("Solução Corporativa de Análise de Sentimentos e Resposta Automática Híbrida")

# Status do Servidor Docker na Barra Lateral
api_online = check_api_health()
with st.sidebar:
    st.header("⚙️ Infraestrutura")
    if api_online:
        st.success("Servidor FastAPI: ONLINE")
    else:
        st.error("Servidor FastAPI: OFFLINE")
    st.markdown("---")
    st.caption("Apresentadores: Rafael, Juliano, Henrique e Iago.")

tab_cliente, tab_admin = st.tabs(["🎫 Portal do Cliente", "📊 Dashboards & Logs"])

# =======================================================
# ABA 1: PORTAL DO CLIENTE (INTERATIVIDADE E SIMULAÇÃO)
# =======================================================
with tab_cliente:
    st.header("Novo Chamado de Suporte")
    st.write("Insira os detalhes do seu problema para processamento e triagem imediata pela nossa infraestrutura.")
    
    with st.container(border=True):
        ticket_text = st.text_area("Descreva o seu problema:", placeholder="Ex: Meu sistema está fora do ar...", height=150)
        
        if st.button("Enviar para Triagem Inteligente", type="primary"):
            if len(ticket_text) < 10:
                st.warning("Por favor, forneça uma descrição detalhada de no mínimo 10 caracteres.")
            else:
                with st.spinner("Processando Inteligência Artificial Híbrida..."):
                    try:
                        payload = {"text": ticket_text}
                        response = requests.post(f"{API_URL}/api/v1/analyze", json=payload)
                        
                        if response.status_code == 200:
                            data = response.json()
                            st.markdown("---")
                            st.subheader("🛠| Simulação de Integração com CRM (Visão Dinâmica para a Banca)")
                            
                            col_cliente, col_crm = st.columns(2)
                            
                            with col_cliente:
                                st.markdown("### 🧑‍💻 O que o Cliente Vê")
                                st.success("Seu chamado foi registrado com sucesso! Nossa equipe técnica entrará em contato.")
                                st.caption(f"Protocolo de Atendimento Gerado: #{data['id']}")
                                st.info("Nenhuma camada de IA é revelada ao cliente. A experiência permanece limpa e humanizada.")

                            with col_crm:
                                st.markdown("### 🎧 O que o Atendente Vê (Zendesk / Jira)")
                                
                                priority_label = data.get('priority', 'NORMAL')
                                
                                # Adaptação do visual baseado na resposta estruturada real gerada pelo Gemini
                                if priority_label == "ALTA":
                                    prioridade = "🔴 ALTA (Urgente - SLA de Crise de Infraestrutura)"
                                    cor_borda = "#ff4b4b"
                                    bg_color = "#331a1a"
                                elif priority_label == "BAIXA":
                                    prioridade = "🔵 BAIXA (Solicitação Operacional de Baixo Impacto)"
                                    cor_borda = "#1e90ff"
                                    bg_color = "#1a2633"
                                else:
                                    prioridade = "🟢 NORMAL (Fila Padrão Comercial)"
                                    cor_borda = "#444"
                                    bg_color = "#1e1e1e"
                                
                                st.markdown(f"""
                                <div style="border: 2px solid {cor_borda}; padding: 15px; border-radius: 8px; background-color: {bg_color};">
                                    <h4 style="color: white; margin-top: 0;">Ticket #{data['id']}</h4>
                                    <p style="color: #ccc; margin-bottom: 5px;"><strong>Status:</strong> Aberto | <strong>Prioridade:</strong> {prioridade}</p>
                                    <p style="color: #ccc;"><strong>Triagem NLP (BERT Local):</strong> <code style="color: #ffcc00; background: transparent;">{data['sentiment']}</code> (Confiança: {data['confidence_score']})</p>
                                    <hr style="margin: 10px 0; border-color: #555;">
                                    <p style="color: white; margin-bottom: 5px;"><strong>Descrição Enviada pelo Usuário:</strong><br><i>"{data['text']}"</i></p>
                                    <hr style="margin: 10px 0; border-color: #555;">
                                    <p style="color: white; margin-bottom: 5px;"><strong>🤖 Nota Interna Gerada de Rascunho (IA Generativa):</strong></p>
                                    <p style="color: #00cc66; margin-bottom: 0;"><i>{data['insight']}</i></p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                            st.markdown("<br>", unsafe_allow_html=True)
                            with st.expander("📡 Visão de Engenharia: Ver Payload JSON enviado ao CRM (Webhook)"):
                                st.json({
                                    "event": "ticket_created",
                                    "ticket_id": data['id'],
                                    "routing_metadata": {
                                        "nlp_sentiment": data['sentiment'],
                                        "confidence": data['confidence_score'],
                                        "ai_priority_classification": data.get('priority'),
                                        "routed_to_external_llm": data['routed_to_llm']
                                    },
                                    "ai_suggested_reply_note": data['insight'],
                                    "processing_time_ms": data['processing_time_ms']
                                })
                        else:
                            st.error(f"Falha na API: {response.status_code} - {response.text}")
                    except Exception as e:
                        st.error("Falha de Rede: Não foi possível alcançar a API do microsserviço.")
                        logger.error(f"Erro no front: {e}")

# =======================================================
# ABA 2: MONITORAMENTO ADMINISTRATIVO E HISTÓRICO
# =======================================================
with tab_admin:
    st.header("Monitoramento de Operações")
    
    if st.button("📥 Sincronizar Dados do Banco"):
        try:
            response = requests.get(f"{API_URL}/api/v1/tickets")
            if response.status_code == 200:
                raw_data = response.json()
                
                if not raw_data:
                    st.warning("O banco relacional está vazio atualmente.")
                else:
                    df = pd.DataFrame(raw_data)
                    
                    # --- DASHBOARD DE KPIS OPERACIONAIS ---
                    st.markdown("### 📊 Indicadores em Tempo Real")
                    kpi1, kpi2, kpi3 = st.columns(3)
                    
                    with kpi1:
                        st.metric(label="Total de Chamados Trafegados", value=len(df))
                    with kpi2:
                        chamados_criticos = len(df[df["priority"] == "ALTA"])
                        st.metric(label="🚨 Chamados Críticos (Alta Urgência)", value=chamados_criticos)
                    with kpi3:
                        total_llm = int(df["routed_to_llm"].sum())
                        st.metric(label="💰 Requisições à Nuvem (Tokens)", value=total_llm)
                    
                    st.markdown("---")
                    st.markdown("### Histórico Detalhado")
                    
                    def highlight_priority(val):
                        if val == 'ALTA': return 'background-color: #331a1a; color: #ff4b4b;'
                        if val == 'BAIXA': return 'background-color: #1a2633; color: #1e90ff;'
                        return ''

                    display_df = df[["id", "sentiment", "confidence_score", "priority", "routed_to_llm", "text", "insight"]].copy()
                    display_df.columns = ["ID", "Sentimento", "Confiança", "Prioridade Inteligente", "Roteado LLM?", "Conteúdo", "Insight IA"]
                    
                    st.dataframe(
                        display_df.style.applymap(highlight_priority, subset=["Prioridade Inteligente"]),
                        use_container_width=True,
                        hide_index=True
                    )
            else:
                st.error("Erro ao ler dados da API.")
        except Exception as e:
            st.error(f"Falha ao sincronizar logs: {e}")