import streamlit as st

# Configuração inicial da página
st.set_page_config(page_title="Projeto Alzheimer", layout="wide", initial_sidebar_state="expanded")

# Título e subtítulo
st.title("Projeto Alzheimer")
st.subheader("Análise Exploratória e Mineração de Dados")

# Seção de Participantes
st.markdown("## Participantes do Grupo")
st.markdown("""
- **Eduardo Henrique Spinelli** (800220)
- **Fernando Kiyoshi Kaida** (769667)
- **Gabriel de Souza Cavalca Leite** (813615)
- **Mateus Grota Nishimura Ferro** (771043)
- **Ruan Crysthian Lima Ferraz** (790866)
""")

st.markdown("---")

# Breve descrição da aplicação
st.write("""
Bem-vindo ao Projeto Alzheimer! Esta aplicação interativa em Streamlit foi desenvolvida para explorar 
um dataset abrangente sobre a Doença de Alzheimer, contendo informações demográficas, dados clínicos, 
histórico médico, avaliações cognitivas e outros atributos. Utilize a barra lateral para navegar pelas 
diferentes seções do projeto, que incluem:
- Descrição do Dataset
- Importação e Pré-processamento dos Dados
- Análise de Hipóteses (com gráficos e tarefas de mineração)
- Dashboard Interativo
- Conclusões
""")

