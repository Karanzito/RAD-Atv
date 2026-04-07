import pandas as pd
import numpy as np

# ── 1. CARREGAR O DATASET ──────────────────────────────
df = pd.read_csv("livros.csv", sep=";")
print(f"Shape: {df.shape}")  # (linhas, colunas)

# ── 2. EXPLORAÇÃO INICIAL ─────────────────────────────
print("\n--- HEAD ---")
print(df.head())

print("\n--- INFO ---")
print(df.info())

print("\n--- DESCRIBE ---")
print(df.describe())

# 2.1 Verificar tipos incorretos
# (geralmente 'ano' ou 'isbn' podem vir como object se houver problemas)

# 3. Valores nulos
print("\n--- VALORES NULOS ---")
nulos = df.isnull().sum()
print(nulos)

# 4. Livros com 0 páginas
print("\n--- LIVROS COM 0 PÁGINAS ---")
livros_zero_paginas = df[df["paginas"] == 0]
print(livros_zero_paginas)
print(f"Quantidade: {len(livros_zero_paginas)}")

# 5. Livros por ano
print("\n--- LIVROS POR ANO ---")
livros_por_ano = df["ano"].value_counts().sort_index()
print(livros_por_ano)

# ── 3. LIMPEZA ────────────────────────────────────────
# Preencher nulos de 'ano' com a mediana
mediana_ano = df["ano"].median()
df["ano"] = df["ano"].fillna(mediana_ano).astype(int)

# Remover livros com 0 páginas
df_limpo = df[df["paginas"] > 0].copy()
removidos = len(df) - len(df_limpo)
print(f"\nRegistros removidos (paginas == 0): {removidos}")

# ── 4. TRANSFORMAÇÃO ──────────────────────────────────
# 1. Criar faixa_paginas
df_limpo["faixa_paginas"] = df_limpo["paginas"].apply(
    lambda x: "Curto" if x < 150 else ("Médio" if x <= 350 else "Longo")
)

# 2. Criar década
df_limpo["decada"] = (df_limpo["ano"] // 10) * 10

print("\n--- AMOSTRA APÓS TRANSFORMAÇÃO ---")
print(df_limpo.head())

# ── 5. ANÁLISE (BÔNUS) ────────────────────────────────

# 1. Média de páginas por década
print("\n--- MÉDIA DE PÁGINAS POR DÉCADA ---")
media_paginas_decada = df_limpo.groupby("decada")["paginas"].mean().sort_index()
print(media_paginas_decada)

# 2. Top 10 autores
print("\n--- TOP 10 AUTORES ---")
top_autores = df_limpo["autor"].value_counts().head(10)
print(top_autores)

# 3. Distribuição faixa_paginas após 2010
print("\n--- DISTRIBUIÇÃO (APÓS 2010) ---")
dist_faixa = df_limpo[df_limpo["ano"] > 2010]["faixa_paginas"].value_counts()
print(dist_faixa)

# ── 6. EXPORTAR ───────────────────────────────────────
df_limpo.to_excel("livros_analisados.xlsx", index=False)
print("\n✅ Arquivo exportado com sucesso!")