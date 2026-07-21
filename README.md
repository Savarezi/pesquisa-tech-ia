# ⚡ CyberTech | Painel de Análise de Dados e IA

> Plataforma interativa de coleta de feedback e telemetria de dados voltada para o mercado de tecnologia e inteligência artificial.

## 🛠️ Sobre o Projeto
Este projeto foi desenvolvido como parte de uma aplicação prática de cursos de tecnologia. Ele consiste em um fluxo conversacional inteligente (**Typebot**) para a captação de dados de participantes e um dashboard analítico de alta performance em tempo real (**Streamlit**), integrado com inteligência artificial (**Google Gemini**) para geração de insights e análise de perfil.

---

## 🚀 Tecnologias Utilizadas
* **Python** (Linguagem principal)
* **Streamlit** (Framework para construção do Dashboard Web)
* **Pandas** (Manipulação e estruturação de dados)
* **Google Generative AI (Gemini)** (Motor de análise inteligente de feedbacks)
* **Google Sheets** (Banco de dados em nuvem para persistência dos registros)
* **Typebot** (Interface de chat interativa para captação das respostas)

---

## 📊 Arquitetura e Fluxo de Dados
1. **Coleta:** O usuário interage com o assistente virtual via Typebot e responde às perguntas sobre sua atuação, senioridade e visão sobre o mercado de IA.
2. **Persistência:** As respostas enviadas são gravadas instantaneamente em uma planilha centralizada no **Google Sheets**.
3. **Visualização & Análise:** O **Streamlit** (hospedado na nuvem) consome os dados da planilha em tempo real, exibindo métricas de volume, distribuição de senioridade, feed de participantes e análises executivas geradas pelo **Google Gemini**.

---

## 🌐 Links do Projeto
* **💬 Acessar o Chat (Typebot):** [Clique aqui para responder](https://typebot.co/my-typebot-sdln62x)
* **📊 Acessar o Painel (Streamlit):** [Visualizar Dashboard em tempo real](https://pesquisa-tech-ia-83cbcdnynqhhasczrqou4t.streamlit.app/)

---

## 💻 Como Executar o Projeto Localmente

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git](https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git)
   cd SEU_REPOSITORIO
