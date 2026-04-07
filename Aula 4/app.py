import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px

st.set_page_config(
    page_title="Dashboard de Funcionários",
    layout="wide"
)

st.title("📊 Dashboard de Análise de Funcionários")

@st.cache_data
def carregar_dados():
    dados = {
        "nome": ["Ana", "Bruno", "Carlos", "Daniela", "Eduardo"],
        "idade": [23, 35, 29, np.nan, 40],
        "cidade": ["SP", "RJ", "SP", "MG", "RJ"],
        "salario": [3000, 5000, 4000, 3500, np.nan],
        "data_contratacao": pd.to_datetime([
            "2020-01-10", "2019-03-15", "2021-07-22", "2018-11-30", "2022-05-05"
        ])
    }

    df = pd.DataFrame(dados)

    df["idade"] = df["idade"].fillna(df["idade"].mean())
    df["salario"] = df["salario"].fillna(df["salario"].median())

    df["salario_anual"] = df["salario"] * 12
    df["ano_contratacao"] = df["data_contratacao"].dt.year
    df["categoria_salario"] = df["salario"].apply(
        lambda x: "Alto" if x > 4500 else "Médio" if x > 3000 else "Baixo"
    )

    return df


def tratar_dados(df):
    df["idade"] = df["idade"].fillna(df["idade"].mean())
    df["salario"] = df["salario"].fillna(df["salario"].median())

    df["salario_anual"] = df["salario"] * 12

    if "data_contratacao" in df.columns:
        df["data_contratacao"] = pd.to_datetime(df["data_contratacao"], errors="coerce")
        df["ano_contratacao"] = df["data_contratacao"].dt.year

    df["categoria_salario"] = df["salario"].apply(
        lambda x: "Alto" if x > 4500 else "Médio" if x > 3000 else "Baixo"
    )

    return df


uploaded_file = st.sidebar.file_uploader(
    "Envie um CSV",
    type=["csv"]
)

if uploaded_file is not None:
    
    df = pd.read_csv(uploaded_file)
    df = tratar_dados(df)

else:

    df = carregar_dados()

# Sidebar
st.sidebar.header("🔎 Filtros")

cidades = st.sidebar.multiselect(
    "Selecione a cidade",
    options=df["cidade"].unique(),
    default=df["cidade"].unique()
)

faixa_salario = st.sidebar.slider(
    "Faixa salarial",
    float(df["salario"].min()),
    float(df["salario"].max()),
    (float(df["salario"].min()), float(df["salario"].max()))
)

categoria = st.sidebar.selectbox(
    "Categoria salarial",
    options=["Todas"] + list(df["categoria_salario"].unique())
)

df_filtrado = df[
    (df["cidade"].isin(cidades)) &
    (df["salario"] >= faixa_salario[0]) &
    (df["salario"] <= faixa_salario[1])
]

if categoria != "Todas":
    df_filtrado = df_filtrado[df_filtrado["categoria_salario"] == categoria]


# Métricas
col1, col2, col3 = st.columns(3)

col1.metric("💰 Salário Médio", f"R$ {df_filtrado['salario'].mean():.2f}")
col2.metric("👥 Total Funcionários", df_filtrado.shape[0])
col3.metric("📈 Salário Máximo", f"R$ {df_filtrado['salario'].max():.2f}")

# Dados
st.subheader("📋 Dados")
st.dataframe(df_filtrado, use_container_width=True)

# Gráficos
st.subheader("📊 Análises")

col1, col2 = st.columns(2)

media_cidade = df_filtrado.groupby("cidade")["salario"].mean()
col1.bar_chart(media_cidade)

categoria = df_filtrado["categoria_salario"].value_counts()
col2.bar_chart(categoria)

media_cidade = df_filtrado.groupby(["cidade", "categoria_salario"])["salario"].mean().reset_index()

fig1 = px.bar(
    media_cidade,
    x="cidade",
    y="salario",
    color="categoria_salario",
    barmode="group",
    title="Média Salarial por Cidade",
    hover_data={
        "cidade": True,
        "salario": ":.2f",
        "categoria_salario": True
    }
)

col1.plotly_chart(fig1, use_container_width=True)

categoria_dist = df_filtrado["categoria_salario"].value_counts().reset_index()
categoria_dist.columns = ["categoria", "quantidade"]

fig2 = px.bar(
    categoria_dist,
    x="categoria",
    y="quantidade",
    color="categoria",
    title="Distribuição por Categoria",
    hover_data={"quantidade": True}
)

col2.plotly_chart(fig2, use_container_width=True)

# Pivot
pivot = pd.pivot_table(
    df_filtrado,
    values="salario",
    index="cidade",
    columns="categoria_salario",
    aggfunc="mean"
)

st.dataframe(pivot)

# Download
csv = df_filtrado.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Baixar CSV",
    data=csv,
    file_name="dados_filtrados.csv",
    mime="text/csv"
)

# Upload
st.sidebar.subheader("📂 Upload de CSV")

uploaded_file = st.sidebar.file_uploader(
    "Envie um arquivo",
    type=["csv", "xlsx", "json", "png", "jpg"]
)

if uploaded_file:

    from PIL import Image

    if uploaded_file.name.endswith(".csv"):
        df_upload = pd.read_csv(uploaded_file)
        st.dataframe(df_upload)


        if uploaded_file.name.endswith(("png", "jpg", "jpeg")):
            img = Image.open(uploaded_file)
            st.image(img)

        elif uploaded_file.name.endswith(".csv"):
            df_upload = pd.read_csv(uploaded_file)
            st.dataframe(df_upload)

# # Imagem (para ML)
# from PIL import Image
# img = Image.open(uploaded_file)
# st.image(img)