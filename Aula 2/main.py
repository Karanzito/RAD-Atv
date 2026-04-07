import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import datetime as dt

# ── Configurações visuais ───────────────────────────────
plt.rcParams['figure.figsize'] = (10, 5)
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

print("✅ Bibliotecas importadas com sucesso!")

# ── Criação do Dataset ───────────────────────────────
np.random.seed(42)

produtos = {
    "Dom Casmurro":       ("Literatura", 35.90),
    "O Pequeno Príncipe": ("Infantil",   29.90),
    "Sapiens":            ("Ciências",   54.90),
    "Python para Dados":  ("Tecnologia", 89.90),
    "Clean Code":         ("Tecnologia", 95.00),
    "Harry Potter Vol.1": ("Fantasia",   49.90),
    "Atomic Habits":      ("Autoajuda",  44.90),
    "A Arte da Guerra":   ("Filosofia",  32.00),
    "Cosmos":             ("Ciências",   62.50),
    "Cem Anos de Solidão":("Literatura", 39.90),
}

vendedores = ["Ana Lima", "Carlos Mendes", "Bruno Costa", "Fernanda Rocha"]
regioes    = ["Sudeste", "Sul", "Nordeste", "Norte", "Centro-Oeste"]
datas      = pd.date_range("2024-01-01", "2024-06-30", periods=50)

nomes_prod = np.random.choice(list(produtos.keys()), 50)

dados = {
    "id_venda":   range(1, 51),
    "data":       datas.strftime("%Y-%m-%d"),
    "produto":    nomes_prod,
    "categoria":  [produtos[p][0] for p in nomes_prod],
    "quantidade": np.random.randint(1, 6, 50),
    "preco_unit": [produtos[p][1] for p in nomes_prod],
    "vendedor":   np.random.choice(vendedores, 50),
    "regiao":     np.random.choice(regioes, 50),
}

df = pd.DataFrame(dados)
df["total_venda"] = df["quantidade"] * df["preco_unit"]

# Converter data
df["data"] = pd.to_datetime(df["data"])
df["mes"] = df["data"].dt.month

# Salvar CSV
df.to_csv("vendas_livraria.csv", index=False)

print(f"✅ Dataset criado! Shape: {df.shape}")
print(df.head())

# ── Exploração Inicial ───────────────────────────────
print("\n📋 INFORMAÇÕES")
print(df.info())

print("\n🔍 NULOS:")
print(df.isnull().sum())

print("\n📈 ESTATÍSTICAS:")
print(df[["quantidade", "preco_unit", "total_venda"]].describe())

# ── Análises ───────────────────────────────

# Faturamento total
total = df["total_venda"].sum()
print(f"\n💰 Total: R$ {total:,.2f}")

# Por categoria
cat_fat = df.groupby("categoria")["total_venda"].sum().sort_values(ascending=False)
print("\n📦 Categoria:\n", cat_fat)

# Ranking vendedores
vend_rank = df.groupby("vendedor")["total_venda"].sum().sort_values(ascending=False)
print("\n🏆 Vendedores:\n", vend_rank)

# Top produtos
top_prod = df.groupby("produto")["quantidade"].sum().sort_values(ascending=False).head(3)
print("\n📚 Top produtos:\n", top_prod)

# Ticket médio por região
reg_media = df.groupby("regiao")["total_venda"].mean().sort_values(ascending=False)
print("\n🗺️ Ticket médio região:\n", reg_media)

# Faturamento mensal
fat_mensal = df.groupby("mes")["total_venda"].sum()
print("\n📅 Faturamento mensal:\n", fat_mensal)

# Desafio

# 1. Tendência mensal (linha)
plt.figure(figsize=(8,4))
plt.plot(fat_mensal.index, fat_mensal.values, marker='o')
plt.title("Tendência de Faturamento")
plt.xlabel("Mês")
plt.ylabel("R$")
plt.grid()
plt.show()

# 2. Ticket médio vendedor
ticket_vend = df.groupby("vendedor")["total_venda"].mean().sort_values(ascending=False)
print("\n🎯 Ticket médio vendedor:\n", ticket_vend)

print("Melhor vendedor (ticket médio):", ticket_vend.idxmax())

# 3. Vendas
altas = df[df["total_venda"] > 200]
print("\n🔥 Vendas altas por categoria:\n",
      altas.groupby("categoria")["total_venda"].count())



nulos = pd.DataFrame({
    "id_venda": range(51, 56),
    "data": [np.nan]*5,
    "produto": [np.nan]*5,
    "categoria": [np.nan]*5,
    "quantidade": [np.nan]*5,
    "preco_unit": [np.nan]*5,
    "vendedor": [np.nan]*5,
    "regiao": [np.nan]*5,
    "total_venda": [np.nan]*5,
    "mes": [np.nan]*5
})

df = pd.concat([df, nulos], ignore_index=True)

print("\nNulos:")
print(df.isnull().sum())


df_drop = df.dropna()


df_fill = df.fillna({
    "quantidade": 0,
    "preco_unit": 0,
    "total_venda": 0,
    "categoria": "Desconhecido",
    "produto": "Desconhecido",
    "vendedor": "Desconhecido",
    "regiao": "Desconhecido"
})


fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Categoria
axes[0].barh(cat_fat.index, cat_fat.values)
axes[0].set_title("Categoria")

# Vendedores
axes[1].bar(vend_rank.index, vend_rank.values)
axes[1].set_title("Vendedores")
axes[1].tick_params(axis="x", rotation=15)

# Regiões
reg_total = df.groupby("regiao")["total_venda"].sum()
axes[2].pie(reg_total, labels=reg_total.index, autopct="%1.1f%%")

plt.tight_layout()
plt.savefig("dashboard.png")
plt.show()