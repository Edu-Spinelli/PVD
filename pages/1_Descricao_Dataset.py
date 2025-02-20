import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch


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



#Plotar gráficos - Detalhes Demográficos
fig, ax = plt.subplots(2,2,figsize=(16, 10))

hachuras1 = ["/", "\\"]
hachuras2 = ["/", "\\", "o", "x"]

fig.suptitle("Detalhes Demográficos")

sns.histplot(data, x="Age", ax=ax[0,0], kde=True, bins=30)
ax[0,0].set_title("Distribuição da Idade (Anos)")
ax[0,0].set_xlabel("Age")
ax[0,0].set_ylabel("Frequência")

c = sns.countplot(data, x="Gender", hue="Gender", ax=ax[0,1], palette=["#ff2626", "#2664ff"])
ax[0,1].set_title("Distribuição do Gênero")
ax[0,1].set_xlabel("Gender")
ax[0,1].set_ylabel("Frequência")
patches = [
    Patch(facecolor="#ff2626", hatch="//", label = "Masculino"),
    Patch(facecolor="#2664ff", hatch="\\\\", label = "Feminino")
]
ax[0,1].legend(title="Gênero", loc="upper right", handles=patches)
for i, bar in enumerate(c.patches):
  bar.set_hatch(hachuras1[i%len(hachuras1)])


c = sns.countplot(data, x="Ethnicity", hue="Ethnicity", ax=ax[1,0], palette="Set2")
ax[1,0].set_title("Distribuição da Etnicidade")
ax[1,0].set_xlabel("Ethnicity")
ax[1,0].set_ylabel("Frequência")
patches = [
    Patch(facecolor="#72b6a1", hatch="//", label = "Caucasiana"),
    Patch(facecolor="#e99675", hatch="//", label = "Afro-Americana"),
    Patch(facecolor="#95a3c3", hatch="o", label = "Asiática"),
    Patch(facecolor="#db96c0", hatch="x", label = "Outras")
]
ax[1,0].legend(title="Etnicidade", loc="upper right", handles=patches)
for i, bar in enumerate(c.patches):
  bar.set_hatch(hachuras2[i%len(hachuras2)])

c = sns.countplot(data, x="EducationLevel", hue="EducationLevel", ax=ax[1,1], palette="Set3")
ax[1,1].set_title("Distribuição do Nível Educacional")
ax[1,1].set_xlabel("EducationLevel")
ax[1,1].set_ylabel("Frequência")
patches = [
    Patch(facecolor="#96cac1", hatch="//", label = "Nenhum"),
    Patch(facecolor="#f6f6bc", hatch="//", label = "Ensino Médio"),
    Patch(facecolor="#c1bed6", hatch="o", label = "Bachalerado"),
    Patch(facecolor="#ea8e83", hatch="x", label = "Superior")
]
ax[1,1].legend(title="Nível Educacional", loc="upper right", handles=patches)

for i, bar in enumerate(c.patches):
  bar.set_hatch(hachuras2[i%len(hachuras2)])

fig.tight_layout()
st.pyplot(fig)

#Plotar Gráficos - Fatores de Estilo de Vida
fig, ax = plt.subplots(2,3,figsize=(16, 10))

fig.suptitle("Fatores de Estilo de Vida")

sns.histplot(data, x="BMI", ax=ax[0,0], kde=True, bins=30, color="green")
ax[0,0].set_title("Distribuição do IMC")
ax[0,0].set_xlabel("BMI")
ax[0,0].set_ylabel("Frequência")

c = sns.countplot(data, x="Smoking", hue="Smoking", ax=ax[0,1], palette=["#ff2626", "#2664ff"])
ax[0,1].set_title("Distribuição dos Fumantes")
ax[0,1].set_xlabel("Smoking")
ax[0,1].set_ylabel("Frequência")
patches = [
    Patch(facecolor="#ff2626", hatch="//", label = "Não"),
    Patch(facecolor="#2664ff", hatch="\\\\", label = "Sim")
]
ax[0,1].legend(title="Fumante?", loc="upper right", handles=patches)
for i, bar in enumerate(c.patches):
  bar.set_hatch(hachuras1[i%len(hachuras1)])

sns.histplot(data, x="AlcoholConsumption", ax=ax[0,2], kde=True, bins=30, color="purple")
ax[0,2].set_title("Distribuição do Consumo de Álcool (Unidades)")
ax[0,2].set_xlabel("AlcoholConsumption")
ax[0,2].set_ylabel("Frequência")

sns.histplot(data, x="PhysicalActivity", ax=ax[1,0], kde=True, bins=30, color="orange")
ax[1,0].set_title("Distribuição da Atividade Física Semanal (Horas)")
ax[1,0].set_xlabel("PhysicalActivity")
ax[1,0].set_ylabel("Frequência")

sns.histplot(data, x="DietQuality", ax=ax[1,1], kde=True, bins=30, color="pink")
ax[1,1].set_title("Distribuição da Qualidade da Dieta (Score)")
ax[1,1].set_xlabel("DietQuality")
ax[1,1].set_ylabel("Frequência")

sns.histplot(data, x="SleepQuality", ax=ax[1,2], kde=True, bins=30, color="brown")
ax[1,1].set_title("Distribuição da Qualidade do Sono (Score)")
ax[1,1].set_xlabel("SleepQuality")
ax[1,1].set_ylabel("Frequência")

fig.tight_layout()
st.pyplot(fig)

#Plotar Gráficos - Histórico Médico
fig, ax = plt.subplots(2,3,figsize=(16, 10))

fig.suptitle("Histórico Médico")

c = sns.countplot(data, x="FamilyHistoryAlzheimers", hue="FamilyHistoryAlzheimers", ax=ax[0,0], palette=["#ff2626","#2664ff"])
ax[0,0].set_title("Distribuição do histórico de Alzheimer na família")
ax[0,0].set_xlabel("FamilyHistoryAlzheimers")
ax[0,0].set_ylabel("Frequência")
patches = [
    Patch(facecolor="#ff2626", hatch="//", label = "Não"),
    Patch(facecolor="#2664ff", hatch="\\\\", label = "Sim")
]
ax[0,0].legend(title="Histórico de Alzheimer?", loc="upper right", handles=patches)
for i, bar in enumerate(c.patches):
  bar.set_hatch(hachuras1[i%len(hachuras1)])


c = sns.countplot(data, x="CardiovascularDisease", hue="CardiovascularDisease", ax=ax[0,1], palette="Set2")
ax[0,1].set_title("Distribuição da presença de Doença Cardiovascular")
ax[0,1].set_xlabel("CardiovascularDisease")
ax[0,1].set_ylabel("Frequência")
patches = [
    Patch(facecolor="#72b6a1", hatch="//", label = "Não"),
    Patch(facecolor="#e99675", hatch="\\\\", label = "Sim")
]
ax[0,1].legend(title="Doença Cardiovascular?", loc="upper right", handles=patches)
for i, bar in enumerate(c.patches):
  bar.set_hatch(hachuras1[i%len(hachuras1)])

c = sns.countplot(data, x="Diabetes", hue="Diabetes", ax=ax[0,2], palette="Set3")
ax[0,2].set_title("Distribuição da presença de Diabetes")
ax[0,2].set_xlabel("Diabetes")
ax[0,2].set_ylabel("Frequência")
patches = [
    Patch(facecolor="#96cac1", hatch="//", label = "Não"),
    Patch(facecolor="#f6f6bc", hatch="\\\\", label = "Sim")
]
ax[0,2].legend(title="Presença de Diabetes?", loc="upper right", handles=patches)
for i, bar in enumerate(c.patches):
  bar.set_hatch(hachuras1[i%len(hachuras1)])

c = sns.countplot(data, x="Depression", hue="Depression", ax=ax[1,0], palette=["#ff13ed","#ffed13"])
ax[1,0].set_title("Distribuição da presença de Depressão")
ax[1,0].set_xlabel("Depression")
ax[1,0].set_ylabel("Frequência")
patches = [
    Patch(facecolor="#ff13ed", hatch="//", label = "Não"),
    Patch(facecolor="#ffed13", hatch="\\\\", label = "Sim")
]
ax[1,0].legend(title="Presença de Depressão?", loc="upper right", handles=patches)
for i, bar in enumerate(c.patches):
  bar.set_hatch(hachuras1[i%len(hachuras1)])

c = sns.countplot(data, x="HeadInjury", hue="HeadInjury", ax=ax[1,1], palette=["#49ff13", "#1c4fee"])
ax[1,1].set_title("Distribuição do histórico de Ferimento na Cabeça")
ax[1,1].set_xlabel("HeadInjury")
ax[1,1].set_ylabel("Frequência")
patches = [
    Patch(facecolor="#49ff13", hatch="//", label = "Não"),
    Patch(facecolor="#1c4fee", hatch="\\\\", label = "Sim")
]
ax[1,1].legend(title="Ferimento na Cabeça?", loc="upper right", handles=patches)
for i, bar in enumerate(c.patches):
  bar.set_hatch(hachuras1[i%len(hachuras1)])

c = sns.countplot(data, x="Hypertension", hue="Hypertension", ax=ax[1,2], palette=["#16f4ed","#9d580b"])
ax[1,2].set_title("Distribuição de presença de Hipertensão")
ax[1,2].set_xlabel("Hypertension")
ax[1,2].set_ylabel("Frequência")
patches = [
    Patch(facecolor="#16f4ed", hatch="//", label = "Não"),
    Patch(facecolor="#9d580b", hatch="\\\\", label = "Sim")
]
ax[1,2].legend(title="Presença de Hipertensão?", loc="upper right", handles=patches)
for i, bar in enumerate(c.patches):
  bar.set_hatch(hachuras1[i%len(hachuras1)])

fig.tight_layout()
st.pyplot(fig)

#Plotar Gráficos - Medições Clínicas
fig, ax = plt.subplots(2,3,figsize=(16, 10))

fig.suptitle("Medições Clínicas")

sns.histplot(data, x="SystolicBP", ax=ax[0,0],kde=True, bins=30, color="#ff2626")
ax[0,0].set_title("Distribuição da Pressão Sistólica (mmHg)")
ax[0,0].set_xlabel("SystolicBP")
ax[0,0].set_ylabel("Frequência")

sns.histplot(data, x="DiastolicBP", ax=ax[0,1],kde=True, bins=30, color="#2664ff")
ax[0,1].set_title("Distribuição da Pressão Diastólica (mmHg)")
ax[0,1].set_xlabel("DiastolicBP")
ax[0,1].set_ylabel("Frequência")

sns.histplot(data, x="CholesterolTotal", ax=ax[0,2],kde=True, bins=30, color="#eb9d2d")
ax[0,2].set_title("Distribuição do Nível de Colesterol Total (mg/dL)")
ax[0,2].set_xlabel("CholesterolTotal")
ax[0,2].set_ylabel("Frequência")

sns.histplot(data, x="CholesterolLDL", ax=ax[1,0],kde=True, bins=30, color="#4fea34")
ax[1,0].set_title("Distribuição da Nível de Colesterol LDL (mg/dL)")
ax[1,0].set_xlabel("CholesterolLDL")
ax[1,0].set_ylabel("Frequência")

sns.histplot(data, x="CholesterolHDL", ax=ax[1,1],kde=True, bins=30, color="#7e2de5")
ax[1,1].set_title("Distribuição da Nível de Colesterol HDL (mg/dL)")
ax[1,1].set_xlabel("CholesterolLDL")
ax[1,1].set_ylabel("Frequência")

sns.histplot(data, x="CholesterolTriglycerides", ax=ax[1,2],kde=True, bins=30, color="#9d580b")
ax[1,2].set_title("Distribuição da Nível de Triglicerídeos (mg/dL)")
ax[1,2].set_xlabel("CholesterolTriglycerides")
ax[1,2].set_ylabel("Frequência")

fig.tight_layout()
st.pyplot(fig)

#Plotar Gráficos - Avaliações Cognitivas e Funcionais
fig, ax = plt.subplots(2,3,figsize=(16, 10))

fig.suptitle("Avaliações Cognitivas e Funcionais")

sns.histplot(data, x="MMSE", ax=ax[0,0],kde=True, bins=30, color="#ff2626")
ax[0,0].set_title("Distribuição do Mini-Exame do Estado Mental (Score)")
ax[0,0].set_xlabel("MMSE")
ax[0,0].set_ylabel("Frequência")

sns.histplot(data, x="FunctionalAssessment", ax=ax[0,1],kde=True, bins=30, color="#2664ff")
ax[0,1].set_title("Distribuição da Avaliação Funcional (Score)")
ax[0,1].set_xlabel("FunctionalAssessment")
ax[0,1].set_ylabel("Frequência")

c = sns.countplot(data, x="MemoryComplaints", hue="MemoryComplaints", ax=ax[0,2], palette=["#ff2626","#2664ff"])
ax[0,2].set_title("Distribuição da presença de Queixas de Memória")
ax[0,2].set_xlabel("MemoryComplaints")
ax[0,2].set_ylabel("Frequência")
patches = [
    Patch(facecolor="#ff2626", hatch="//", label = "Não"),
    Patch(facecolor="#2664ff", hatch="\\\\", label = "Sim")
]
ax[0,2].legend(title="Queixas de Memória?", loc="upper right", labels=["Não", "Sim"])
for i, bar in enumerate(c.patches):
  bar.set_hatch(hachuras1[i%len(hachuras1)])

c = sns.countplot(data, x="BehavioralProblems", hue="BehavioralProblems", ax=ax[1,0], palette=["#49ff13", "#1c4fee"])
ax[1,0].set_title("Distribuição de Problemas Comportamentais")
ax[1,0].set_xlabel("BehavioralProblems")
ax[1,0].set_ylabel("Frequência")
patches = [
    Patch(facecolor="#49ff13", hatch="//", label = "Não"),
    Patch(facecolor="#1c4fee", hatch="\\\\", label = "Sim")
]
ax[1,0].legend(title="Problemas Comportamentais?", loc="upper right", handles=patches)
for i, bar in enumerate(c.patches):
  bar.set_hatch(hachuras1[i%len(hachuras1)])

sns.histplot(data, x="ADL", ax=ax[1,1],kde=True, bins=30, color="#eb9d2d")
ax[1,1].set_title("Distribuição das Atividades de Vida Diária (Score)")
ax[1,1].set_xlabel("ADL")
ax[1,1].set_ylabel("Frequência")

fig.delaxes(ax=ax[1,2])

fig.tight_layout()
st.pyplot(fig)

#Plotar Gráficos - Sintomas e Diagnóstico
fig, ax = plt.subplots(2,3,figsize=(16, 10))

fig.suptitle("Sintomas e Diagnóstico")

c = sns.countplot(data, x="Confusion", hue="Confusion", ax=ax[0,0], palette=["#ff2626","#2664ff"])
ax[0,0].set_title("Distribuição da presença de Confusão")
ax[0,0].set_xlabel("Confusion")
ax[0,0].set_ylabel("Frequência")
patches = [
    Patch(facecolor="#ff2626", hatch="//", label = "Não"),
    Patch(facecolor="#2664ff", hatch="\\\\", label = "Sim")
]
ax[0,0].legend(title="Confusão?", loc="upper right", handles=patches)
for i, bar in enumerate(c.patches):
  bar.set_hatch(hachuras1[i%len(hachuras1)])


c = sns.countplot(data, x="Disorientation", hue="Disorientation", ax=ax[0,1], palette="Set2")
ax[0,1].set_title("Distribuição da presença de Desorientação")
ax[0,1].set_xlabel("Disorientation")
ax[0,1].set_ylabel("Frequência")
patches = [
    Patch(facecolor="#72b6a1", hatch="//", label = "Não"),
    Patch(facecolor="#e99675", hatch="\\\\", label = "Sim")
]
ax[0,1].legend(title="Presença de Desorientação?", loc="upper right", handles=patches)
for i, bar in enumerate(c.patches):
  bar.set_hatch(hachuras1[i%len(hachuras1)])

c = sns.countplot(data, x="PersonalityChanges", hue="PersonalityChanges", ax=ax[0,2], palette="Set3")
ax[0,2].set_title("Distribuição de Mudanças de Personalidade")
ax[0,2].set_xlabel("PersonalityChanges")
ax[0,2].set_ylabel("Frequência")
patches = [
    Patch(facecolor="#96cac1", hatch="//", label = "Não"),
    Patch(facecolor="#f6f6bc", hatch="\\\\", label = "Sim")
]
ax[0,2].legend(title="Mudanças?", loc="upper right", handles=patches)
for i, bar in enumerate(c.patches):
  bar.set_hatch(hachuras1[i%len(hachuras1)])

c = sns.countplot(data, x="DifficultyCompletingTasks", hue="DifficultyCompletingTasks", ax=ax[1,0], palette=["#ff13ed","#ffed13"])
ax[1,0].set_title("Distribuição de Dificuldade de Completar Tarefas")
ax[1,0].set_xlabel("DifficultyCompletingTasks")
ax[1,0].set_ylabel("Frequência")
patches = [
    Patch(facecolor="#ff13ed", hatch="//", label = "Não"),
    Patch(facecolor="#ffed13", hatch="\\\\", label = "Sim")
]
ax[1,0].legend(title="Dificuldades?", loc="upper right", handles=patches)
for i, bar in enumerate(c.patches):
  bar.set_hatch(hachuras1[i%len(hachuras1)])

c = sns.countplot(data, x="Forgetfulness", hue="Forgetfulness", ax=ax[1,1], palette=["#49ff13", "#1c4fee"])
ax[1,1].set_title("Distribuição da presença de Esquecimento")
ax[1,1].set_xlabel("Forgetfulness")
ax[1,1].set_ylabel("Frequência")
patches = [
    Patch(facecolor="#49ff13", hatch="//", label = "Não"),
    Patch(facecolor="#1c4fee", hatch="\\\\", label = "Sim")
]
ax[1,1].legend(title="Presença de Esquecimento?", loc="upper right", handles=patches)
for i, bar in enumerate(c.patches):
  bar.set_hatch(hachuras1[i%len(hachuras1)])

c = sns.countplot(data, x="Diagnosis", hue="Diagnosis", ax=ax[1,2], palette=["#16f4ed","#9d580b"])
ax[1,2].set_title("Distribuição do Diagnóstico")
ax[1,2].set_xlabel("Diagnosis")
ax[1,2].set_ylabel("Frequência")
patches = [
    Patch(facecolor="#16f4ed", hatch="//", label = "Não"),
    Patch(facecolor="#9d580b", hatch="\\\\", label = "Sim")
]
ax[1,2].legend(title="Presença de Alzheimer?", loc="upper right", handles=patches)
for i, bar in enumerate(c.patches):
  bar.set_hatch(hachuras1[i%len(hachuras1)])

fig.tight_layout()
st.pyplot(fig)