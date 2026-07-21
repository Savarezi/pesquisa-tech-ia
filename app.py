import json
import os
import google.generativeai as genai
import pandas as pd
import streamlit as st





# Pega a chave direto do cofre de segredos do Streamlit
api_key = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=api_key)
# ==========================================
# INSIRA SUA CHAVE DA API DO GEMINI AQUI:
# ==========================================


# Configura a chave
api_key = os.environ.get("GEMINI_API_KEY") or SUA_CHAVE_API
if api_key and api_key != "SUA_CHAVE_AQUI":
  genai.configure(api_key=api_key)

# Configuração da página
st.set_page_config(
    page_title="CyberTech | Dev Dark Terminal", page_icon="💻", layout="wide"
)

# Estilização Dark Dev limpa e sem elementos brancos
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&family=Inter:wght@400;600;700&display=swap');

    .stApp {
        background-color: #090d16;
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Topo estilo Terminal / IDE */
    .dev-header {
        font-family: 'Fira Code', monospace;
        background: #0d1322;
        border: 1px solid #1e293b;
        border-left: 4px solid #10b981;
        padding: 15px 20px;
        border-radius: 8px;
        color: #38bdf8;
        font-size: 0.95rem;
        margin-bottom: 25px;
    }

    .main-title {
        font-family: 'Fira Code', monospace;
        color: #f8fafc;
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -1px;
    }
    .main-title span {
        color: #10b981;
    }

    /* Cards de Métricas estilo Dev */
    .metric-card {
        background: #0d1322;
        border: 1px solid #1e293b;
        border-radius: 8px;
        padding: 18px;
        text-align: left;
        font-family: 'Fira Code', monospace;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
    }
    .metric-title {
        font-size: 0.75rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-value {
        font-size: 1.4rem;
        font-weight: 600;
        color: #10b981;
        margin-top: 5px;
    }

    /* Cards de Status / Telemetria no lugar do gráfico */
    .telemetry-card {
        background: #0d1322;
        border: 1px solid #1e293b;
        border-radius: 8px;
        padding: 20px;
        font-family: 'Fira Code', monospace;
        height: 100%;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .telemetry-title {
        color: #38bdf8;
        font-size: 0.9rem;
        margin-bottom: 12px;
        border-bottom: 1px solid #1e293b;
        padding-bottom: 8px;
    }

    /* Card individual para cada Participante */
    .participante-card {
        background: #0d1322;
        border: 1px solid #1e293b;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .dev-tag {
        font-family: 'Fira Code', monospace;
        background: #1e293b;
        color: #38bdf8;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 0.7rem;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Cabeçalho estilo Terminal
st.markdown(
    """
    <div class="dev-header">
        root@cybertech-ai:~# ./initialize_dashboard.sh --env=production --theme=dark-dev
    </div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    "<h1 class='main-title'>⚡ cybertech<span>.analytics</span>()</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='color: #64748b; font-family: Fira Code, monospace; font-size:"
    " 0.9rem;'>// Painel de inteligência de dados e feedback de"
    " participantes</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

ARQUIVO_JSON = "respostas.json"


def carregar_dados():
  if not os.path.exists(ARQUIVO_JSON):
    return pd.DataFrame()
  try:
    with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
      conteudo = f.read().strip()
      if not conteudo:
        return pd.DataFrame()
      dados = json.loads(conteudo)
      if isinstance(dados, list):
        return pd.DataFrame(dados)
      elif isinstance(dados, dict):
        return pd.DataFrame([dados])
  except Exception as e:
    st.error(f"Erro ao ler os dados: {e}")
    return pd.DataFrame()


df = carregar_dados()

# Botão de Reset discreto no topo
col_top1, col_top2 = st.columns([6, 1])
with col_top2:
  if st.button("🗑️ Resetar", use_container_width=True):
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
      json.dump([], f)
    st.rerun()

if df.empty:
  st.markdown(
      """
        <div style='text-align: center; padding: 50px; background: #0d1322; border-radius: 8px; border: 1px dashed #334155;'>
            <h3 style='font-family: Fira Code; color: #38bdf8;'>[ 404 ] Nenhum dado encontrado</h3>
            <p style='color: #64748b; font-family: Fira Code;'>Aguardando payloads de respostas via Typebot...</p>
        </div>
    """,
      unsafe_allow_html=True,
  )
else:
  total_respostas = len(df)
  principal_area = (
      df["area"].mode()[0] if "area" in df.columns and not df.empty else "N/A"
  )
  senioridade_comum = (
      df["senioridade"].mode()[0]
      if "senioridade" in df.columns and not df.empty
      else "N/A"
  )

  # Métricas principais no topo
  m1, m2, m3 = st.columns(3)
  with m1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">// total_respostas</div>
            <div class="metric-value">{total_respostas}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
  with m2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">// area_principal</div>
            <div class="metric-value" style="font-size: 1.1rem; color: #38bdf8;">{principal_area}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
  with m3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">// senioridade_mode</div>
            <div class="metric-value" style="font-size: 1.1rem; color: #c084fc;">{senioridade_comum}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

  st.markdown("<br>", unsafe_allow_html=True)

  # --- ANÁLISE DA IA COM FILTRO POR NOME DO PARTICIPANTE ---
  with st.expander(
      "🤖 [ Central de Análise Inteligente com Filtro por Participante ]",
      expanded=False,
  ):
    st.markdown(
        "<p style='color: #94a3b8; font-size: 0.85rem;'>Selecione um"
        " participante específico para gerar a análise focada na resposta"
        " dele:</p>",
        unsafe_allow_html=True,
    )

    lista_nomes = (
        df["nome"].tolist() if "nome" in df.columns else ["Participante"]
    )
    opcoes_filtro = ["🌐 Analisar Geral (Todas as Respostas)"] + lista_nomes
    participante_selecionado = st.selectbox(
        "Filtrar Análise por Participante:", opcoes_filtro
    )

    if st.button("🚀 Processar Análise com IA", type="primary"):
      if not api_key or api_key == "SUA_CHAVE_AQUI":
        st.error("⚠️ Insira sua chave da API do Gemini no código.")
      else:
        with st.spinner(
            f"Gerando insights para: {participante_selecionado}..."
        ):
          try:
            if participante_selecionado == "🌐 Analisar Geral (Todas as Respostas)":
              dados_participantes = []
              for _, row in df.iterrows():
                n = row.get("nome", "Participante")
                op = row.get("opiniao_ia", "")
                dados_participantes.append(f"Nome: {n} | Opinião: {op}")
              texto_dados = "\n".join(dados_participantes)
              prompt_ia = (
                  "Aja como um analista tech sênior. Resuma de forma direta"
                  " e limpa os pontos principais destas opiniões gerais de"
                  f" todos os participantes:\n\n{texto_dados}"
              )
            else:
              linha_filtrada = df[df["nome"] == participante_selecionado].iloc[0]
              n = linha_filtrada.get("nome", "Participante")
              email = linha_filtrada.get("email", "")
              area = linha_filtrada.get("area", "")
              senioridade = linha_filtrada.get("senioridade", "")
              opiniao = linha_filtrada.get("opiniao_ia", "")

              prompt_ia = (
                  "Aja como um analista tech sênior. Faça uma análise crítica,"
                  " técnica e executiva focada exclusivamente na resposta e"
                  f" perfil deste participante:\n- Nome: {n}\n- Área:"
                  f" {area}\n- Senioridade: {senioridade}\n- Opinião/Resposta"
                  f" enviada: {opiniao}"
              )

            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt_ia)

            st.markdown(
                f"<div"
                f" style='background:#020617;padding:15px;border-radius:6px;border:1px"
                f" solid #334155;color:#f8fafc; margin-top: 10px;'><b"
                f" style='color:#10b981;'>Análise para: "
                f"{participante_selecionado}</b><br><br>{response.text}</div>",
                unsafe_allow_html=True,
            )
          except Exception as e:
            st.error(f"Erro ao conectar com a IA: {e}")

  st.markdown("<br>", unsafe_allow_html=True)

  # --- TELEMETRIA EM CARDS DARK (Substituindo os gráficos feios) ---
  st.markdown(
      "<h3 style='font-family: Fira Code; color: #38bdf8; font-size:"
      " 1.1rem;'>📊 telemetry.status_overview()</h3>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p style='color: #64748b; font-size: 0.85rem;'>Resumo estruturado de"
      " fluxo e telemetria do sistema.</p>",
      unsafe_allow_html=True,
  )

  col_t1, col_t2 = st.columns(2)

  with col_t1:
    st.markdown(
        f"""
        <div class="telemetry-card">
            <div class="telemetry-title">// Fluxo de Entradas (Volume)</div>
            <p style="color: #94a3b8; font-size: 0.85rem; margin: 8px 0;">Status do Payload: <span style="color: #10b981;">[ OK ] Sincronizado</span></p>
            <p style="color: #94a3b8; font-size: 0.85rem; margin: 8px 0;">Total Registrado: <b style="color: #38bdf8;">{total_respostas} registro(s)</b></p>
            <p style="color: #94a3b8; font-size: 0.85rem; margin: 8px 0;">Último ID na Fila: <b style="color: #c084fc;">#{total_respostas}</b></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

  with col_t2:
    st.markdown(
        f"""
        <div class="telemetry-card">
            <div class="telemetry-title">// Distribuição por Perfil (Senioridade)</div>
            <p style="color: #94a3b8; font-size: 0.85rem; margin: 8px 0;">Nível Predominante: <b style="color: #10b981;">{senioridade_comum}</b></p>
            <p style="color: #94a3b8; font-size: 0.85rem; margin: 8px 0;">Segmento Principal: <b style="color: #38bdf8;">{principal_area}</b></p>
            <p style="color: #94a3b8; font-size: 0.85rem; margin: 8px 0;">Integridade dos Dados: <span style="color: #10b981;">100% estruturados</span></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

  st.markdown("---")

  # --- CARDS INDIVIDUAIS DOS PARTICIPANTES ---
  st.markdown(
      "<h3 style='font-family: Fira Code; color: #38bdf8; font-size:"
      " 1.1rem;'>👥 participantes.feed()</h3>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p style='color: #64748b; font-size: 0.85rem;'>Cards individuais com as"
      " respostas enviadas por cada participante.</p>",
      unsafe_allow_html=True,
  )

  for index, row in df.iterrows():
    nome_pessoa = row.get("nome", f"Participante {index + 1}")
    email_pessoa = row.get("email", "Não informado")
    cidade_pessoa = row.get("cidade", "Não informada")
    area_pessoa = row.get("area", "Não informada")
    senioridade_pessoa = row.get("senioridade", "Não informada")
    opiniao_pessoa = row.get(
        "opiniao_ia", "Nenhuma opinião detalhada fornecida."
    )

    st.markdown(
        f"""
        <div class="participante-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <h4 style="font-family: Fira Code; color: #10b981; margin: 0; font-size: 1.05rem;">👤 {nome_pessoa}</h4>
                <span class="dev-tag">id_#{index + 1}</span>
            </div>
            <p style="color: #94a3b8; font-size: 0.82rem; margin: 2px 0;"><b>Email:</b> {email_pessoa}</p>
            <p style="color: #94a3b8; font-size: 0.82rem; margin: 2px 0;"><b>Local:</b> {cidade_pessoa} | <b>Área:</b> {area_pessoa} | <b>Senioridade:</b> {senioridade_pessoa}</p>
            <hr style="border-color: #1e293b; margin: 8px 0;">
            <p style="color: #64748b; font-size: 0.7rem; text-transform: uppercase; font-family: Fira Code;"><b>Opinião Registrada:</b></p>
            <p style="color: #e2e8f0; background: #020617; padding: 10px; border-radius: 6px; border: 1px solid #1e293b; font-size: 0.88rem; white-space: pre-wrap; margin-bottom: 0;">{opiniao_pessoa}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )