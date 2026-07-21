# Importa as bibliotecas necessárias
import google.generativeai as genai
import pandas as pd
import streamlit as st


# ============================================================
# CONFIGURAÇÃO DA API DO GEMINI
# ============================================================

# Pega a chave diretamente dos Secrets do Streamlit
api_key = st.secrets["GEMINI_API_KEY"]

# Configura a API do Gemini
genai.configure(api_key=api_key)


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Painel de Análise de Dados", page_icon="💻", layout="wide"
)


# ============================================================
# ESTILIZAÇÃO VISUAL DO SISTEMA
# ============================================================

st.markdown(
    """
    <style>

    /* Importa fontes modernas */
    @import url(
        'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap'
    );

    /* Variáveis de cores */
    :root {
        --bg-primary: #070b14;
        --border: rgba(148, 163, 184, 0.14);
        --text-primary: #f8fafc;
        --green: #34d399;
        --blue: #38bdf8;
        --purple: #a78bfa;
    }

    /* Fundo principal */
    .stApp {
        background:
            radial-gradient(
                circle at 10% 0%,
                rgba(56, 189, 248, 0.08),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(167, 139, 250, 0.08),
                transparent 30%
            ),
            var(--bg-primary);

        color: var(--text-primary);
        font-family: 'DM Sans', sans-serif;
    }

    /* Esconde menu padrão do Streamlit */
    #MainMenu {
        visibility: hidden;
    }

    /* Esconde rodapé */
    footer {
        visibility: hidden;
    }

    /* ========================================================
       TÍTULO PRINCIPAL
       ======================================================== */

    .main-title {
        font-family: 'DM Sans', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        letter-spacing: -1.5px;
        color: #ffffff;
        margin-bottom: 0;
    }

    .main-title span {
        background: linear-gradient(
            90deg,
            #34d399,
            #38bdf8,
            #a78bfa
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* ========================================================
       CARDS DE MÉTRICAS
       ======================================================== */

    .metric-card {
        position: relative;
        overflow: hidden;

        background: linear-gradient(
            145deg,
            rgba(17, 25, 40, 0.92),
            rgba(10, 15, 27, 0.92)
        );

        border: 1px solid var(--border);
        border-radius: 18px;

        padding: 24px;

        min-height: 130px;

        box-shadow:
            0 20px 40px rgba(0, 0, 0, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.03);

        transition: all 0.25s ease;
    }

    .metric-card:hover {
        transform: translateY(-4px);

        border-color: rgba(56, 189, 248, 0.35);

        box-shadow:
            0 25px 50px rgba(0, 0, 0, 0.35),
            0 0 25px rgba(56, 189, 248, 0.08);
    }

    .metric-title {
        color: #64748b;

        font-family: 'Space Mono', monospace;

        font-size: 0.72rem;

        text-transform: uppercase;

        letter-spacing: 1px;

        margin-bottom: 12px;
    }

    .metric-value {
        font-family: 'DM Sans', sans-serif;

        font-size: 1.7rem;

        font-weight: 700;

        color: var(--green);

        line-height: 1.3;
    }

    .area-value {
        color: var(--blue) !important;
        font-size: 1.1rem !important;
    }

    .senioridade-value {
        color: var(--purple) !important;
        font-size: 1.1rem !important;
    }

    /* ========================================================
       CARDS DE TELEMETRIA
       ======================================================== */

    .telemetry-card {
        height: 100%;

        background: rgba(15, 23, 42, 0.72);

        border: 1px solid var(--border);

        border-radius: 18px;

        padding: 24px;

        backdrop-filter: blur(18px);

        box-shadow:
            0 18px 40px rgba(0, 0, 0, 0.22);

        transition: all 0.25s ease;
    }

    .telemetry-card:hover {
        transform: translateY(-3px);

        border-color: rgba(167, 139, 250, 0.3);
    }

    .telemetry-title {
        color: var(--blue);

        font-family: 'Space Mono', monospace;

        font-size: 0.85rem;

        margin-bottom: 18px;

        padding-bottom: 12px;

        border-bottom: 1px solid var(--border);
    }

    /* ========================================================
       CARDS DOS PARTICIPANTES
       ======================================================== */

    .participante-card {
        background:
            linear-gradient(
                145deg,
                rgba(17, 25, 40, 0.86),
                rgba(10, 15, 27, 0.86)
            );

        border: 1px solid var(--border);

        border-radius: 16px;

        padding: 18px;

        margin-bottom: 14px;

        transition: all 0.25s ease;
    }

    .participante-card:hover {
        transform: translateX(5px);

        border-color: rgba(52, 211, 153, 0.35);

        box-shadow:
            0 12px 30px rgba(0, 0, 0, 0.25);
    }

    /* Tag do ID */
    .dev-tag {
        background: rgba(56, 189, 248, 0.1);

        border: 1px solid rgba(56, 189, 248, 0.25);

        color: var(--blue);

        padding: 4px 9px;

        border-radius: 999px;

        font-family: 'Space Mono', monospace;

        font-size: 0.68rem;
    }

    /* ========================================================
       SELECTBOX
       ======================================================== */

    div[data-baseweb="select"] > div {
        background: rgba(15, 23, 42, 0.85) !important;

        border: 1px solid var(--border) !important;

        border-radius: 12px !important;

        min-height: 44px;

        transition: all 0.2s ease;
    }

    div[data-baseweb="select"] > div:hover {
        border-color: rgba(56, 189, 248, 0.5) !important;
    }

    div[data-baseweb="select"] span {
        color: #e2e8f0 !important;
    }

    div[data-baseweb="popover"],
    div[data-baseweb="menu"] {
        background: #0f172a !important;

        border: 1px solid #334155 !important;

        border-radius: 12px !important;
    }

    li[role="option"]:hover {
        background: rgba(56, 189, 248, 0.12) !important;

        color: #38bdf8 !important;
    }

    /* ========================================================
       BOTÕES
       ======================================================== */

    .stButton > button {
        border-radius: 10px;

        border: 1px solid rgba(52, 211, 153, 0.35);

        background:
            linear-gradient(
                135deg,
                rgba(52, 211, 153, 0.18),
                rgba(56, 189, 248, 0.12)
            );

        color: #f8fafc;

        font-weight: 600;

        transition: all 0.25s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);

        border-color: #34d399;

        box-shadow:
            0 8px 25px rgba(52, 211, 153, 0.18);
    }

    /* ========================================================
       EXPANDER
       ======================================================== */

    [data-testid="stExpander"] {
        background: rgba(15, 23, 42, 0.65);

        border: 1px solid var(--border);

        border-radius: 16px;
    }

    /* Divisórias */
    hr {
        border-color: rgba(148, 163, 184, 0.12);
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CABEÇALHO
# ============================================================

st.markdown(
    "<h1 class='main-title'>⚡ Painel <span>de Análise</span></h1>",
    unsafe_allow_html=True,
)

st.markdown(
    "<p style='color: #64748b; font-family: Space Mono, monospace; font-size:"
    " 0.9rem;'>// Inteligência de dados e feedback de participantes</p>",
    unsafe_allow_html=True,
)

st.markdown("---")


# ============================================================
# LINK DA PLANILHA
# ============================================================

SHEET_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1t7UbKfQA61zz7Xm_2x7AbwxieJmMoY_cIb9sN9N4upI"
    "/edit?usp=sharing"
)


# ============================================================
# FUNÇÃO PARA CARREGAR OS DADOS
# ============================================================


def carregar_dados():

    try:

        if not SHEET_URL:

            return pd.DataFrame()

        # Converte o link do Google Sheets para CSV
        csv_url = SHEET_URL

        if "/edit" in SHEET_URL:

            csv_url = (
                SHEET_URL.rsplit("/edit", 1)[0] + "/export?format=csv"
            )

        # Lê os dados da planilha
        df = pd.read_csv(csv_url)

        return df

    except Exception as e:

        st.error(f"Erro ao ler os dados da planilha: {e}")

        return pd.DataFrame()


# Carrega os dados
df = carregar_dados()


# ============================================================
# VERIFICA SE EXISTEM DADOS
# ============================================================

if df.empty:

    st.markdown(
        """
        <div style='
            text-align: center;
            padding: 50px;
            background: #0d1322;
            border-radius: 16px;
            border: 1px dashed #334155;
        '>

            <h3 style='
                font-family: Space Mono;
                color: #38bdf8;
            '>

                [ 404 ] Nenhum dado encontrado

            </h3>

            <p style='
                color: #64748b;
                font-family: Space Mono;
            '>

                Verifique se a planilha tem dados
                ou se está pública para leitura...

            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )


else:

    # ========================================================
    # CALCULA AS MÉTRICAS PRINCIPAIS
    # ========================================================

    total_respostas = len(df)

    principal_area = (
        df["area"].mode()[0]
        if "area" in df.columns and not df.empty
        else "N/A"
    )

    senioridade_comum = (
        df["senioridade"].mode()[0]
        if "senioridade" in df.columns and not df.empty
        else "N/A"
    )

    # ========================================================
    # MÉTRICAS PRINCIPAIS
    # ========================================================

    m1, m2, m3 = st.columns(3)

    # Card: total de respostas
    with m1:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-title">
                    // total_respostas
                </div>

                <div class="metric-value">
                    {total_respostas}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    # Card: área principal
    with m2:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-title">
                    // area_principal
                </div>

                <div class="metric-value area-value">
                    {principal_area}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    # Card: senioridade mais comum
    with m3:

        st.markdown(
            f"""
            <div class="metric-card">

                <div class="metric-title">
                    // senioridade_mode
                </div>

                <div class="metric-value senioridade-value">
                    {senioridade_comum}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ========================================================
    # CENTRAL DE ANÁLISE DA IA
    # ========================================================

    with st.expander("🤖 Central de Análise Inteligente", expanded=False):

        st.markdown(
            """
            <p style='
                color: #94a3b8;
                font-size: 0.85rem;
            '>

                Selecione um participante específico
                para gerar uma análise focada.

            </p>
            """,
            unsafe_allow_html=True,
        )

        # Cria a lista de nomes
        lista_nomes = (
            df["nome"].tolist() if "nome" in df.columns else ["Participante"]
        )

        # Adiciona opção de análise geral
        opcoes_filtro = ["🌐 Analisar Geral (Todas as Respostas)"] + lista_nomes

        # Selectbox para selecionar o participante
        participante_selecionado = st.selectbox(
            "Filtrar Análise por Participante:", opcoes_filtro
        )

        # Botão que executa a análise
        if st.button("🚀 Processar Análise com IA", type="primary"):

            # Verifica a chave da API
            if not api_key or api_key == "SUA_CHAVE_AQUI":

                st.error("⚠️ Insira sua chave da API do Gemini no código.")

            else:

                with st.spinner(
                    f"Gerando insights para: {participante_selecionado}..."
                ):

                    try:

                        # ====================================================
                        # ANÁLISE GERAL
                        # ====================================================

                        if (
                            participante_selecionado
                            == "🌐 Analisar Geral (Todas as Respostas)"
                        ):

                            dados_participantes = []

                            for _, row in df.iterrows():

                                n = row.get("nome", "Participante")
                                op = row.get("opiniao_ia", "")

                                dados_participantes.append(
                                    f"Nome: {n} | Opinião: {op}"
                                )

                            texto_dados = "\n".join(dados_participantes)

                            prompt_ia = (
                                "Aja como um analista tech sênior. "
                                "Resuma de forma direta e limpa os "
                                "pontos principais destas opiniões "
                                f"gerais de todos os participantes:\n\n{texto_dados}"
                            )

                        # ====================================================
                        # ANÁLISE INDIVIDUAL
                        # ====================================================

                        else:

                            linha_filtrada = df[
                                df["nome"] == participante_selecionado
                            ].iloc[0]

                            n = linha_filtrada.get("nome", "Participante")
                            area = linha_filtrada.get("area", "")
                            senioridade = linha_filtrada.get("senioridade", "")
                            opiniao = linha_filtrada.get("opiniao_ia", "")

                            prompt_ia = (
                                "Aja como um analista tech sênior. "
                                "Faça uma análise crítica, técnica "
                                "e executiva focada exclusivamente "
                                "na resposta e perfil deste participante:"
                                f"\n- Nome: {n}"
                                f"\n- Área: {area}"
                                f"\n- Senioridade: {senioridade}"
                                f"\n- Opinião/Resposta enviada: {opiniao}"
                            )

                        # Cria o modelo do Gemini
                        model = genai.GenerativeModel("gemini-2.5-flash")

                        # Envia o prompt para a IA
                        response = model.generate_content(prompt_ia)

                        # Exibe o resultado da análise
                        st.markdown(
                            f"""
                            <div style='
                                background:
                                    linear-gradient(
                                        145deg,
                                        rgba(17, 25, 40, 0.95),
                                        rgba(2, 6, 23, 0.95)
                                    );

                                padding: 20px;

                                border-radius: 16px;

                                border: 1px solid
                                    rgba(56, 189, 248, 0.18);

                                color: #f8fafc;

                                margin-top: 10px;

                                line-height: 1.7;

                                box-shadow:
                                    0 15px 35px
                                    rgba(0, 0, 0, 0.25);
                            '>

                                <b style='color:#34d399;'>

                                    Análise para:
                                    {participante_selecionado}

                                </b>

                                <br><br>

                                {response.text}

                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    except Exception as e:

                        st.error(f"Erro ao conectar com a IA: {e}")

    st.markdown("<br>", unsafe_allow_html=True)

    # ========================================================
    # VISÃO GERAL DO STATUS
    # ========================================================

    st.markdown(
        """
        <h3 style='
            font-family: Space Mono;
            color: #38bdf8;
            font-size: 1.1rem;
        '>

            📊 Visão Geral do Status &
            Distribuição por Senioridade

        </h3>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <p style='
            color: #64748b;
            font-size: 0.85rem;
        '>

            Resumo estruturado de fluxo e contagem
            detalhada por nível técnico.

        </p>
        """,
        unsafe_allow_html=True,
    )

    # Conta quantos participantes existem por senioridade
    if "senioridade" in df.columns:

        contagem_senioridade = df["senioridade"].value_counts()

    else:

        contagem_senioridade = pd.Series()

    # Cria duas colunas
    col_t1, col_t2 = st.columns(2)

    # ========================================================
    # CARD DE FLUXO DE ENTRADAS
    # ========================================================

    with col_t1:

        st.markdown(
            f"""
            <div class="telemetry-card">

                <div class="telemetry-title">

                    // Fluxo de Entradas (Volume)

                </div>

                <p style='
                    color: #94a3b8;
                    font-size: 0.85rem;
                '>

                    Status do Payload:

                    <span style='color: #34d399;'>

                        [ OK ] Sincronizado

                    </span>

                </p>

                <p style='
                    color: #94a3b8;
                    font-size: 0.85rem;
                '>

                    Total Registrado:

                    <b style='color: #38bdf8;'>

                        {total_respostas} registro(s)

                    </b>

                </p>

                <p style='
                    color: #94a3b8;
                    font-size: 0.85rem;
                '>

                    Segmento Principal:

                    <b style='color: #34d399;'>

                        {principal_area}

                    </b>

                </p>

            </div>
            """,
            unsafe_allow_html=True,
        )

    # ========================================================
    # CARD DE CONTAGEM POR SENIORIDADE
    # ========================================================

    with col_t2:

        linhas_senioridades = ""

        if not contagem_senioridade.empty:

            for nivel, qtd in contagem_senioridade.items():

                linhas_senioridades += f"""

                <p style="
                    color: #94a3b8;
                    font-size: 0.85rem;
                    margin: 6px 0;
                ">

                    • {nivel}:

                    <b style="color: #c084fc;">

                        {qtd} participante(s)

                    </b>

                </p>

                """

        else:

            linhas_senioridades = """

            <p style="
                color: #94a3b8;
                font-size: 0.85rem;
            ">

                Nenhum dado de senioridade
                registrado ainda.

            </p>

            """

        st.markdown(
            f"""

            <div class="telemetry-card">

                <div class="telemetry-title">

                    // Contagem por Senioridade

                </div>

                {linhas_senioridades}

            </div>

            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ========================================================
    # FEED DOS PARTICIPANTES
    # ========================================================

    st.markdown(
        """
        <h3 style='
            font-family: Space Mono;
            color: #38bdf8;
            font-size: 1.1rem;
        '>

            👥 Feed de Participantes

        </h3>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <p style='
            color: #64748b;
            font-size: 0.85rem;
        '>

            Cards compactos com as respostas
            enviadas por cada participante.

        </p>
        """,
        unsafe_allow_html=True,
    )

    # Percorre cada participante da planilha
    for index, row in df.iterrows():

        nome_pessoa = row.get("nome", f"Participante {index + 1}")

        email_pessoa = row.get("email", "Não informado")

        cidade_pessoa = row.get("cidade", "Não informada")

        area_pessoa = row.get("area", "Não informada")

        senioridade_pessoa = row.get("senioridade", "Não informada")

        opiniao_pessoa = row.get(
            "opiniao_ia", "Nenhuma opinião detalhada fornecida."
        )

        # Exibe o card de cada participante
        st.markdown(
            f"""

            <div class="participante-card">

                <div style="
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 8px;
                ">

                    <span style="
                        color: #34d399;
                        font-size: 1rem;
                        font-weight: 700;
                    ">

                        👤 {nome_pessoa}

                    </span>

                    <span class="dev-tag">

                        id_#{index + 1}

                    </span>

                </div>

                <div style="
                    color: #94a3b8;
                    font-size: 0.78rem;
                    margin-bottom: 10px;
                    line-height: 1.8;
                ">

                    <b>Email:</b> {email_pessoa}

                    &nbsp; | &nbsp;

                    <b>Local:</b> {cidade_pessoa}

                    &nbsp; | &nbsp;

                    <b>Área:</b> {area_pessoa}

                    &nbsp; | &nbsp;

                    <b>Senioridade:</b> {senioridade_pessoa}

                </div>

                <div style="
                    color: #e2e8f0;
                    background: rgba(2, 6, 23, 0.75);
                    padding: 12px 14px;
                    border-radius: 10px;
                    border: 1px solid
                        rgba(148, 163, 184, 0.1);
                    font-size: 0.82rem;
                    white-space: pre-wrap;
                    line-height: 1.6;
                ">

                    <span style="
                        color: #64748b;
                        font-size: 0.68rem;
                        text-transform: uppercase;
                        font-family: 'Space Mono';
                        display: block;
                        margin-bottom: 4px;
                    ">

                        Opinião Registrada:

                    </span>

                    {opiniao_pessoa}

                </div>

            </div>

            """,
            unsafe_allow_html=True,
        )