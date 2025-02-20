import streamlit as st
import pandas as pd

# Configuração da página
st.title("Pré-Processamento dos Dados")

# Caminho para o dataset
DATA_PATH = "data/alzheimers_disease_data.csv"

# Tenta carregar o arquivo
try:
    data = pd.read_csv(DATA_PATH)
    st.success("Dados carregados com sucesso!")
except FileNotFoundError:
    st.error(f"Erro: O arquivo {DATA_PATH} não foi encontrado. Verifique se o caminho está correto.")
    st.stop()

# Exibir as primeiras linhas do dataset original
st.subheader("Prévia do Conjunto de Dados Original")
st.write(data.head())

# -----------------------------
# 1. Remoção de Colunas Irrelevantes
# -----------------------------
st.subheader("Remoção de Colunas Irrelevantes")

# Definir as colunas a serem removidas
columns_to_remove = ["PatientID", "DoctorInCharge"]

# Verificar se as colunas existem antes de remover
existing_columns_to_remove = [col for col in columns_to_remove if col in data.columns]

if existing_columns_to_remove:
    data.drop(columns=existing_columns_to_remove, inplace=True)
    st.success(f"As colunas {existing_columns_to_remove} foram removidas com sucesso!")
else:
    st.warning("Nenhuma coluna relevante foi encontrada para remoção.")

# -----------------------------
# 2. Exibição dos Dados Após o Pré-Processamento
# -----------------------------
st.subheader("Prévia dos Dados Após o Pré-Processamento")
st.write(data.head())

# -----------------------------
# 3. Opção para Baixar os Dados Tratados
# -----------------------------
st.subheader("Baixar os Dados Processados")

# Criar um botão para baixar os dados tratados
csv = data.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Baixar CSV dos Dados Tratados",
    data=csv,
    file_name="dados_tratados.csv",
    mime="text/csv"
)
