from sklearn.discriminant_analysis import StandardScaler
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from scipy.stats import ttest_ind
from matplotlib.patches import Patch

from scipy.special import expit
import numpy as np

# Configuração da página
st.title("Validação das Hipóteses")

# Caminho para os dados tratados
DATA_PATH = "data/dados_tratados.csv"

# Carregar os dados
try:
    data = pd.read_csv(DATA_PATH)
    st.success("Dados carregados com sucesso!")
except FileNotFoundError:
    st.error(f"Erro: O arquivo {DATA_PATH} não foi encontrado. Certifique-se de rodar o pré-processamento antes.")
    st.stop()

st.markdown("---")



# -----------------------------
# 4.1 - Hipótese 1: Tabagismo e Colesterol HDL
# -----------------------------
st.header("4.1 - Tabagismo e Colesterol HDL")

st.write("""
**Hipótese:** Fumantes possuem menores níveis de colesterol HDL.

**Gráficos Utilizados:** Strip Plot, Boxplot, Regressão Logística e Distribuição Acumulada (CDF)
""")

# Criar gráficos lado a lado
fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# Stripplot com símbolos diferentes para fumantes e não fumantes
sns.stripplot(x="Smoking", y="CholesterolHDL", data=data, ax=ax[0], jitter=0.2, palette="Set1", marker='s', label="Não Fumante")
sns.stripplot(x="Smoking", y="CholesterolHDL", data=data, ax=ax[0], jitter=0.2, palette="Set1", marker='^', label="Fumante")
ax[0].set_title("Relação entre Fumo e Colesterol HDL")
ax[0].set_xlabel("Fumante (0 = Não, 1 = Sim)")
ax[0].set_ylabel("Colesterol HDL")
ax[0].legend()

# Boxplot com padrões visuais para acessibilidade
box = sns.boxplot(x="Smoking", y="CholesterolHDL", data=data, ax=ax[1], palette="Set2")
ax[1].set_title("Distribuição de Colesterol HDL entre Fumantes e Não-Fumantes")
ax[1].set_xlabel("Fumante (0 = Não, 1 = Sim)")
ax[1].set_ylabel("Colesterol HDL")

# Adicionando padrões visuais nos boxplots
for i, patch in enumerate(box.patches):
    if i % 2 == 0:
        patch.set_hatch("//")  # Listras
    else:
        patch.set_hatch("o")  # Bolinhas

st.pyplot(fig)

# Explicação detalhada dos gráficos
st.markdown("""
**Explicação dos Gráficos:**

O primeiro gráfico (Strip Plot) apresenta a relação entre tabagismo e colesterol HDL, onde cada ponto representa um paciente. 
Foram utilizados símbolos distintos (quadrado para não fumantes e triângulo para fumantes) para melhorar a acessibilidade visual. 
Caso a hipótese fosse verdadeira, seria esperado que os valores do colesterol HDL fossem visivelmente menores para fumantes.

O segundo gráfico (Boxplot) exibe a distribuição do colesterol HDL para fumantes e não fumantes, com padrões visuais diferentes 
(listras e bolinhas) para cada grupo. Esse gráfico permite uma visualização clara da mediana e da dispersão dos dados.
""")

# Regressão Logística
X = data["CholesterolHDL"].values.reshape(-1, 1)
y = data["Smoking"]
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
clf = LogisticRegression(random_state=0).fit(x_train, y_train)

# Criando gráfico de regressão logística
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(data=data, x="CholesterolHDL", y="Smoking", palette="colorblind", hue=True, legend=False, ax=ax)

textstr = f'β1: {round(float(clf.coef_[0][0]), 3)}'
props = dict(boxstyle='round', facecolor='white', alpha=0.5)
ax.text(0.95, 0.7, textstr, transform=ax.transAxes, fontsize=12,
        verticalalignment='center', horizontalalignment='right', bbox=props)

x_test_range = np.linspace(20, 100, 300)
loss = expit(x_test_range * clf.coef_ + clf.intercept_).ravel()
plt.plot(x_test_range, loss, label="Logistic Regression Model", color='red', linewidth=3)
plt.xlabel("CholesterolHDL")
plt.ylabel("Smoking")
plt.legend()
st.pyplot(fig)

st.markdown("""
**Explicação da Regressão Logística:**

A regressão logística foi usada para verificar a relação entre tabagismo e colesterol HDL. O valor do coeficiente β1 indica o impacto do colesterol HDL sobre a probabilidade de um indivíduo ser fumante.

Se β1 fosse negativo e significativo, validaria a hipótese de que fumantes possuem menor colesterol HDL. No entanto, β1 = -0.003, mostrando que não há diferença estatisticamente relevante entre fumantes e não fumantes.
""")


# Criar distribuição acumulada (CDF)
fig, ax = plt.subplots(figsize=(8, 5))
sns.ecdfplot(data=data, x="CholesterolHDL", hue="Smoking", palette=["blue", "red"], ax=ax)
ax.set_title("Função de Distribuição Acumulada - CholesterolHDL vs Smoking")
ax.set_xlabel("Nível de Colesterol HDL")
ax.set_ylabel("Probabilidade Acumulada")
ax.legend(title="Fumante", labels=["Não", "Sim"])
st.pyplot(fig)

st.markdown("""
**Análise da Distribuição Acumulada (CDF):**
- A CDF permite visualizar a diferença na distribuição de colesterol HDL entre fumantes e não fumantes.
- Se a curva dos fumantes estiver mais à esquerda, indica menores níveis de colesterol HDL.
- Caso contrário, não há evidência significativa de diferença entre os grupos.
""")


st.markdown("---")


# -----------------------------
# 4.2 - Hipótese 2: Histórico Familiar e Diagnóstico de Alzheimer
# -----------------------------
st.header("4.2 - Histórico Familiar e Diagnóstico de Alzheimer")

st.write("""
**Hipótese:** Pacientes com histórico familiar de Alzheimer possuem maior probabilidade de diagnóstico positivo.

**Gráficos Utilizados:** Gráfico de Barras e Função de Densidade de Probabilidade (PDF)


""")

# Criar gráfico de barras com padrões visuais alternados
fig, ax = plt.subplots(figsize=(8, 6))

# Definição de padrões visuais alternados
patterns = ["//", "//", "o", "o"]  # Alternância entre listras e bolinhas
colors = ["gray", "blue"]

# Criar barras
bars = sns.countplot(x="FamilyHistoryAlzheimers", hue="Diagnosis", data=data, ax=ax, palette=colors)
ax.set_title("Histórico Familiar vs. Diagnóstico")
ax.set_xlabel("Histórico Familiar (0 = Não, 1 = Sim)")
ax.set_ylabel("Contagem")

# Aplicando padrões alternados para cada barra
for i, bar in enumerate(bars.patches):
    bar.set_hatch(patterns[i % len(patterns)])

# Criando legenda com padrões visuais
legend_patches = [
    Patch(facecolor=colors[0], hatch="//", label="Hist. Familiar - Negativo (0)"),
    Patch(facecolor=colors[0], hatch="o", label="Hist. Familiar - Positivo (1)"),
    Patch(facecolor=colors[1], hatch="//", label="Diagnóstico Negativo"),
    Patch(facecolor=colors[1], hatch="o", label="Diagnóstico Positivo")
]
ax.legend(handles=legend_patches, title="Legenda")

st.pyplot(fig)

# Explicação detalhada do gráfico de barras
st.markdown("""
**Explicação do Gráfico:**

O gráfico de barras mostra a distribuição de diagnósticos de Alzheimer entre pacientes com e sem histórico familiar. 
As barras foram personalizadas com padrões visuais alternados para tornar a distinção mais acessível. Pacientes sem histórico familiar (0)
apresentam uma maior quantidade de diagnósticos negativos em comparação com positivos. Já pacientes com histórico familiar (1)
também apresentam uma quantidade maior de diagnósticos negativos do que positivos, mas a diferença entre os grupos não é tão expressiva visualmente.
""")

# Criar Pair Plot
fig = sns.pairplot(data, vars=['FamilyHistoryAlzheimers', 'Diagnosis'], hue="FamilyHistoryAlzheimers", palette="husl", height=3)
st.pyplot(fig.fig)

# Explicação do Pair Plot
st.markdown("""
**Explicação do Pair Plot:**

O Pair Plot exibe diferentes relações entre as variáveis FamilyHistoryAlzheimers e Diagnosis. 
No entanto, a separação entre os pontos não indica uma correlação forte entre histórico familiar e diagnóstico positivo para Alzheimer.
""")

# Regressão Logística
X = data[["FamilyHistoryAlzheimers"]]
y = data["Diagnosis"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
log_reg = LogisticRegression()
log_reg.fit(X_train, y_train)
y_pred = log_reg.predict(X_test)

# Criar gráfico de regressão logística
fig, ax = plt.subplots(figsize=(8, 6))
plt.scatter(data['FamilyHistoryAlzheimers'], data['Diagnosis'], color='blue', alpha=0.5, label="Dados Observados")
X_test_range = np.linspace(0, 1, 500).reshape(-1, 1)
y_prob = expit(X_test_range * log_reg.coef_[0][0] + log_reg.intercept_[0])
plt.plot(X_test_range, y_prob, color='red', linewidth=2, label="Curva Logística")
plt.title("Regressão Logística: Diagnóstico x Histórico Familiar", fontsize=14)
plt.xlabel("FamilyHistoryAlzheimers (0 = Não, 1 = Sim)", fontsize=12)
plt.ylabel("Probabilidade de Diagnóstico Positivo", fontsize=12)
plt.legend()
st.pyplot(fig)

# Explicação da regressão logística
st.markdown("""
**Explicação da Regressão Logística:**

A regressão logística foi aplicada para verificar se o histórico familiar influencia o diagnóstico de Alzheimer. 
O coeficiente β1 obtido na regressão é próximo de zero, indicando que o histórico familiar tem um impacto muito pequeno 
ou inexistente sobre a probabilidade de um diagnóstico positivo.

Portanto, a hipótese é **refutada**.
""")

# Criar gráfico de densidade (PDF)
fig, ax = plt.subplots(figsize=(8, 5))
sns.kdeplot(data=data, x="Diagnosis", hue="FamilyHistoryAlzheimers", fill=True, palette=["gray", "blue"], ax=ax)
ax.set_title("Função de Densidade de Probabilidade - Diagnóstico de Alzheimer vs Histórico Familiar")
ax.set_xlabel("Diagnóstico de Alzheimer (0 = Negativo, 1 = Positivo)")
ax.set_ylabel("Densidade de Probabilidade")
ax.legend(title="Histórico Familiar", labels=["Não", "Sim"])
st.pyplot(fig)

st.markdown("""
**Análise da Função de Densidade de Probabilidade (PDF):**
- A PDF mostra a distribuição de probabilidade dos diagnósticos de Alzheimer entre pacientes com e sem histórico familiar.
- Se a curva dos pacientes com histórico familiar estiver mais deslocada para diagnósticos positivos, isso indicaria uma correlação.
- Caso contrário, não há uma relação estatisticamente significativa.
""")



st.markdown("---")



# -----------------------------
# 4.3 - Hipótese 3: Qualidade da Dieta e MMSE
# -----------------------------
st.header("4.3 - Qualidade da Dieta e MMSE")

st.write("""
**Hipótese:** Uma melhor qualidade da dieta está associada a escores mais altos no MMSE.

**Gráficos Utilizados:** Gráfico de Dispersão, Regressão Linear e Histograma.
""")

# Gráfico de dispersão
fig, ax = plt.subplots(figsize=(3, 2))
p = sns.jointplot(data=data, x="DietQuality", y="MMSE", kind="scatter", marginal_kws=dict(bins=30, fill=False))
p.fig.suptitle("DietQuality x MMSE")
p.fig.tight_layout()
p.fig.text(0.5, -0.05, "O gráfico de dispersão posiciona as amostras no espaço dos atributos DietQuality e MMSE nos eixos X e Y acompanhado de suas distribuições. Não é possível observar visualmente nenhuma tendência.", wrap=True, horizontalalignment='center')
st.pyplot(p.fig)

# Regressão Linear
X = data[["DietQuality"]]
Y = data[["MMSE"]]
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

clf = LinearRegression().fit(x_train, y_train)

y_pred = clf.predict(x_test)

# Gráfico de regressão linear
fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(x=x_test.values.reshape(1,-1)[0], y=y_test.values.reshape(1,-1)[0], label="Dados Reais")
sns.scatterplot(x=x_test.values.reshape(1,-1)[0], y=y_pred.reshape(1,-1)[0], label="Previsões")
plt.title("Regressão Linear - DietQuality x MMSE")
plt.xlabel("DietQuality")
plt.ylabel("MMSE")
st.pyplot(fig)


# Histograma adicional
fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(data, x="DietQuality", kde=True, bins=30, color="blue", alpha=0.5)
ax.set_title("Histograma - Distribuição da Qualidade da Dieta")
ax.set_xlabel("Qualidade da Dieta")
ax.set_ylabel("Frequência")
st.pyplot(fig)

# Explicação detalhada
st.markdown(f"""
**Análise dos Gráficos e Mineração de Dados**

- Se a hipótese for verdadeira, veremos uma correlação positiva entre **DietQuality** e **MMSE**.
- O coeficiente da **Regressão Linear** foi **{clf.coef_[0][0]:.4f}**.
- Como é muito próximo de zero, a hipótese foi **refutada**.
""")





st.markdown("---")

# -----------------------------
# 4.4 - Hipótese 4: Atividade Física e Sintomas Cognitivos
# -----------------------------
st.header("4.4 - Atividade Física e Sintomas Cognitivos")

st.write("""
**Hipótese:** Pacientes mais ativos apresentam menos sintomas cognitivos.

**Gráficos Utilizados:** Boxplot, Teste T e Função de Distribuição Acumulada (CDF)
""")

# Criando os boxplots com destaque para as medianas
fig, ax = plt.subplots(1, 2, figsize=(14, 6))

# Boxplot para Confusion
sns.boxplot(data=data, x='Confusion', y='PhysicalActivity', showfliers=False, palette='pastel', ax=ax[0])
medians_confusion = data.groupby('Confusion')['PhysicalActivity'].median()
for i, median in enumerate(medians_confusion):
    ax[0].text(i, median + 0.1, f"{median:.2f}", ha='center', color='blue', fontsize=10)
ax[0].set_title('Atividade Física vs Confusion')
ax[0].set_xlabel('Confusion (0: Não, 1: Sim)')
ax[0].set_ylabel('Atividade Física')

# Boxplot para Forgetfulness
sns.boxplot(data=data, x='Forgetfulness', y='PhysicalActivity', showfliers=False, palette='pastel', ax=ax[1])
medians_forgetfulness = data.groupby('Forgetfulness')['PhysicalActivity'].median()
for i, median in enumerate(medians_forgetfulness):
    ax[1].text(i, median + 0.1, f"{median:.2f}", ha='center', color='blue', fontsize=10)
ax[1].set_title('Atividade Física vs Forgetfulness')
ax[1].set_xlabel('Forgetfulness (0: Não, 1: Sim)')
ax[1].set_ylabel('Atividade Física')

st.pyplot(fig)

# Explicação detalhada dos gráficos
st.markdown("""
**Análise dos Boxplots:**

- A distribuição de atividade física é analisada em relação aos sintomas de **Confusion** e **Forgetfulness**.
- Medianas destacadas mostram pequenas diferenças entre os grupos.
- Se a hipótese for verdadeira, a atividade física dos pacientes sem sintomas deve ser visivelmente maior.
""")

# Histogramas
fig, ax = plt.subplots(1, 2, figsize=(12, 6))

# Histograma para PhysicalActivity por Confusion
sns.histplot(data=data, x="PhysicalActivity", hue="Confusion", kde=True, multiple="stack", palette="Set2", ax=ax[0])
ax[0].set_title('Distribuição de PhysicalActivity por Confusion')
ax[0].set_xlabel('Physical Activity (0 a 10)')
ax[0].set_ylabel('Frequência')

# Histograma para PhysicalActivity por Forgetfulness
sns.histplot(data=data, x="PhysicalActivity", hue="Forgetfulness", kde=True, multiple="stack", palette="Set2", ax=ax[1])
ax[1].set_title('Distribuição de PhysicalActivity por Forgetfulness')
ax[1].set_xlabel('Physical Activity (0 a 10)')
ax[1].set_ylabel('Frequência')

st.pyplot(fig)






# Teste T de Student
st.subheader("Análise Estatística - Teste T")

# Teste T para Confusion
group0 = data[data['Confusion'] == 0]['PhysicalActivity']
group1 = data[data['Confusion'] == 1]['PhysicalActivity']
t_stat, p_value = ttest_ind(group0, group1)
st.write(f"**Teste T para Confusion**: t-statistic = {t_stat:.3f}, p-value = {p_value:.4f}")
if p_value < 0.05:
    st.write("- Diferença significativa entre os grupos")
else:
    st.write("- Sem diferença significativa entre os grupos")

# Teste T para Forgetfulness
group0 = data[data['Forgetfulness'] == 0]['PhysicalActivity']
group1 = data[data['Forgetfulness'] == 1]['PhysicalActivity']
t_stat, p_value = ttest_ind(group0, group1)
st.write(f"**Teste T para Forgetfulness**: t-statistic = {t_stat:.3f}, p-value = {p_value:.4f}")
if p_value < 0.05:
    st.write("- Diferença significativa entre os grupos")
else:
    st.write("- Sem diferença significativa entre os grupos")
    
    
# Criar distribuição acumulada (CDF)
fig, ax = plt.subplots(figsize=(8, 5))
sns.ecdfplot(data=data, x="PhysicalActivity", hue="Confusion", palette=["blue", "red"], ax=ax)
ax.set_title("Função de Distribuição Acumulada - Atividade Física vs Sintomas Cognitivos")
ax.set_xlabel("Atividade Física")
ax.set_ylabel("Probabilidade Acumulada")
ax.legend(title="Sintomas Cognitivos", labels=["Não", "Sim"])
st.pyplot(fig)    

st.markdown("""
**Análise da Distribuição Acumulada (CDF):**
- A CDF permite visualizar a diferença na distribuição de atividade física entre pacientes com e sem sintomas cognitivos.
- Se a curva dos pacientes com sintomas estiver mais à esquerda, indica menor nível de atividade física.
- Caso contrário, não há evidência significativa de diferença entre os grupos.
""")


st.markdown("---")


# -----------------------------
# 4.5 - Hipótese 5: Atividade Física e Depressão
# -----------------------------
st.header("4.5 - Atividade Física e Depressão")

st.write("""
**Hipótese:** Pacientes com depressão praticam menos atividade física.

**Gráficos Utilizados:** Boxplot, Gráfico de Violino e Teste T
""")

# Criando os boxplots e gráficos de violino
fig, ax = plt.subplots(1, 2, figsize=(14, 6))

# Boxplot para Depressão
sns.boxplot(data=data, x='Depression', y='PhysicalActivity', showfliers=False, palette='coolwarm', ax=ax[0])
medians_depression = data.groupby('Depression')['PhysicalActivity'].median()
for i, median in enumerate(medians_depression):
    ax[0].text(i, median + 0.1, f"{median:.2f}", ha='center', color='blue', fontsize=10)
ax[0].set_title('Atividade Física vs Depressão')
ax[0].set_xlabel('Depression (0: Não, 1: Sim)')
ax[0].set_ylabel('Atividade Física')

# Gráfico de Violino
sns.violinplot(data=data, x='Depression', y='PhysicalActivity', palette='coolwarm', split=True, ax=ax[1])
ax[1].set_title('Distribuição de Atividade Física por Depressão')
ax[1].set_xlabel('Depression (0: Não, 1: Sim)')
ax[1].set_ylabel('Atividade Física')

st.pyplot(fig)

# Explicação detalhada dos gráficos
st.markdown("""
**Análise dos Boxplots e Gráfico de Violino:**

- A distribuição de atividade física foi analisada para pacientes com e sem depressão.
- Medianas destacadas mostram diferenças entre os grupos.
- Se a hipótese for verdadeira, pacientes sem depressão terão maiores níveis médios de atividade física.
""")

# Teste T de Student
st.subheader("Análise Estatística - Teste T")

# Teste T para Depressão
group0 = data[data['Depression'] == 0]['PhysicalActivity']
group1 = data[data['Depression'] == 1]['PhysicalActivity']
t_stat, p_value = ttest_ind(group0, group1)
st.write(f"**Teste T para Depressão**: t-statistic = {t_stat:.3f}, p-value = {p_value:.4f}")
if p_value < 0.05:
    st.write("- Diferença significativa entre os grupos")
else:
    st.write("- Sem diferença significativa entre os grupos")

# Regressão Logística
st.subheader("Regressão Logística")
scaler = StandardScaler()
data['PhysicalActivity_scaled'] = scaler.fit_transform(data[['PhysicalActivity']])

X = data[['PhysicalActivity_scaled']].values
y = data['Depression'].values

model = LogisticRegression()
model.fit(X, y)

beta_0 = model.intercept_[0]
beta_1 = model.coef_[0][0]

st.write(f"**Coeficientes da Regressão Logística:** β0 = {beta_0:.4f}, β1 = {beta_1:.4f}")
if beta_1 < 0:
    st.write("- Hipótese validada: Pacientes com depressão tendem a praticar menos atividade física.")
else:
    st.write("- Hipótese refutada: Não há evidência de que pacientes com depressão pratiquem menos atividade física.")


# Criar a Função de Distribuição Acumulada (CDF)
fig, ax = plt.subplots(figsize=(8, 5))
sns.ecdfplot(data=data, x="PhysicalActivity", hue="Depression", palette=["gray", "blue"], ax=ax)
ax.set_title("Função de Distribuição Acumulada - Atividade Física vs Depressão")
ax.set_xlabel("Atividade Física (0 a 10)")
ax.set_ylabel("Probabilidade Acumulada")
ax.legend(title="Depressão", labels=["Não", "Sim"])
st.pyplot(fig)

st.markdown("""
**Análise da CDF:**

- A CDF permite visualizar a diferença na distribuição de atividade física entre pacientes com e sem depressão.
- Se a curva dos pacientes com depressão estiver mais à esquerda, indica menores níveis de atividade física.
- Caso contrário, não há evidência significativa de diferença entre os grupos.
""")



st.markdown("---")


# Conclusão
st.subheader("Conclusão")
st.write("""
Foi realizada a exploração de uma base de dados sobre a Doença de Alzheimer, utilizando métodos de análise e visualização de dados para investigar possíveis padrões e relações entre os atributos do dataset. Para embasar a formulação de hipóteses relevantes, foi fundamental a descrição detalhada dos dados, incluindo fatores demográficos, histórico médico e avaliações cognitivas.

As hipóteses abordaram questões importantes, como os efeitos do tabagismo nos níveis de colesterol HDL, a influência do histórico familiar no diagnóstico da doença e o impacto de fatores como dieta e atividade física na saúde cognitiva e física. As visualizações desempenham um papel fundamental na comunicação das hipóteses apresentadas, tornando os resultados mais intuitivos e acessíveis.

De maneira geral, o trabalho proporcionou um aprendizado sobre o uso de técnicas de análise e mineração de dados, bem como sobre a importância da qualidade e da organização dos dados para se obter insights.
""")