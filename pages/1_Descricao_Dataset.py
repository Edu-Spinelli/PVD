import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuração da página
st.title("Descrição do Conjunto de Dados")

st.markdown("""
## Sobre o Conjunto de Dados

Este conjunto de dados contém i'nformações abrangentes sobre a saúde de 2.149 pacientes, cada um identificado de forma única com IDs variando de 4751 a 6900. Ele inclui detalhes demográficos, fatores de estilo de vida, histórico médico, medições clínicas, avaliações cognitivas e funcionais, sintomas e um diagnóstico da Doença de Alzheimer.

O objetivo deste conjunto de dados é auxiliar pesquisadores e cientistas de dados na exploração de fatores associados à Doença de Alzheimer, no desenvolvimento de modelos preditivos e na realização de análises estatísticas.

## Estrutura dos Dados

O conjunto de dados está organizado nos seguintes grupos de atributos:

1. **Informações do Paciente**
   - **PatientID**: Identificador único do paciente.
   
2. **Detalhes Demográficos**
   - **Idade**: Varia entre 60 e 90 anos.
   - **Gênero**: 0 = Masculino, 1 = Feminino.
   - **Etnia**: 0 = Caucasiano, 1 = Afro-americano, 2 = Asiático, 3 = Outro.
   - **Nível de Educação**: 0 = Nenhum, 1 = Ensino Médio, 2 = Bacharelado, 3 = Superior.

3. **Fatores de Estilo de Vida**
   - **IMC (Índice de Massa Corporal)**: Varia entre 15 e 40.
   - **Fumante**: 0 = Não, 1 = Sim.
   - **Consumo de Álcool**: Consumo semanal em unidades (0 a 20).
   - **Atividade Física**: Horas de atividade física semanal (0 a 10).
   - **Qualidade da Dieta**: Escala de 0 a 10.
   - **Qualidade do Sono**: Escala de 4 a 10.

4. **Histórico Médico**
   - **Histórico Familiar de Alzheimer**: 0 = Não, 1 = Sim.
   - **Doença Cardiovascular, Diabetes, Depressão, Lesão na Cabeça, Hipertensão**: 0 = Não, 1 = Sim.

5. **Medições Clínicas**
   - **Pressão Arterial Sistólica**: Varia entre 90 e 180 mmHg.
   - **Pressão Arterial Diastólica**: Varia entre 60 e 120 mmHg.
   - **Colesterol Total**: Varia entre 150 e 300 mg/dL.
   - **Colesterol LDL**: Varia entre 50 e 200 mg/dL.
   - **Colesterol HDL**: Varia entre 20 e 100 mg/dL.
   - **Triglicerídeos**: Varia entre 50 e 400 mg/dL.

6. **Avaliações Cognitivas e Funcionais**
   - **Exame do Estado Mental Mini-Mental (MMSE)**: Escore de 0 a 30 (quanto menor, maior o comprometimento cognitivo).
   - **Avaliação Funcional**: Escore de 0 a 10 (quanto menor, maior o comprometimento).
   - **Queixas de Memória e Problemas Comportamentais**: 0 = Não, 1 = Sim.
   - **Atividades da Vida Diária (ADL)**: Escore de 0 a 10 (quanto menor, maior o comprometimento).

7. **Sintomas**
   - **Confusão, Desorientação, Mudanças de Personalidade, Dificuldade em Completar Tarefas, Esquecimento**: 0 = Não, 1 = Sim.

8. **Diagnóstico**
   - **Diagnóstico da Doença de Alzheimer**: 0 = Não, 1 = Sim.

---
""")

st.markdown("### **Link para o Dataset**")
st.markdown("[Acesse o conjunto de dados no Kaggle](https://www.kaggle.com/datasets/rabieelkharoua/alzheimers-disease-dataset)")

st.markdown("---")

# -----------------------------------------------------------
#  Carregamento do Dataset e Plotagem de Histogramas
# -----------------------------------------------------------

st.subheader("Distribuição das Variáveis Numéricas")

# Caminho para o dataset
DATA_PATH = "data/alzheimers_disease_data.csv"

# Tenta carregar o arquivo e exibir erro caso não seja encontrado
try:
    data = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    st.error(f"Erro: O arquivo {DATA_PATH} não foi encontrado. Verifique se o caminho está correto.")
    st.stop()

# Selecionar colunas numéricas
numeric_cols = data.select_dtypes(include=["int64", "float64"]).columns

# Criar um grid para exibir todos os histogramas lado a lado
num_cols = len(numeric_cols)  # Quantidade real de colunas numéricas
num_rows = (num_cols // 6) + (1 if num_cols % 6 != 0 else 0)  # Determinar número correto de linhas

fig, axes = plt.subplots(nrows=num_rows, ncols=6, figsize=(15, 10))  
axes = axes.flatten()  # Converter matriz de eixos em lista

# Plotar histogramas para cada coluna numérica
for i, col in enumerate(numeric_cols):  
    ax = axes[i]
    ax.hist(data[col].dropna(), bins=30, edgecolor="black", color="skyblue")
    ax.set_title(col)
    ax.set_xlabel("Valores")
    ax.set_ylabel("Frequência")

# Ocultar gráficos vazios (se houver)
for i in range(num_cols, len(axes)):
    fig.delaxes(axes[i])  # Remove os eixos vazios

# Ajustar layout para evitar sobreposição
fig.tight_layout()

# Exibir o gráfico no Streamlit
st.pyplot(fig, use_container_width=False)