# ── Importações ──────────────────────────────────────
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# Configurações visuais
plt.rcParams['figure.figsize'] = (10, 5)
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

print("✅ Bibliotecas importadas com sucesso!")


# ── Criação do Dataset ───────────────────────────────
np.random.seed(42)

produtos = {
    "Dom Casmurro":       ("Literatura", 35.90),
    "O Pequeno Príncipe": ("Infantil",   29.90),
    "Sapiens":             ("Ciências",   54.90),
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

# Salva como CSV
df.to_csv("vendas_livraria.csv", index=False)

print(f"✅ Dataset criado! Shape: {df.shape}")
print(f"   Colunas: {list(df.columns)}")
print(df.head())


# ── Exploração Inicial (EDA) ─────────────────────────
df = pd.read_csv("vendas_livraria.csv")

print("═" * 45)
print("📋 INFORMAÇÕES DO DATASET")
print("═" * 45)
print(f"Linhas:   {df.shape[0]}")
print(f"Colunas:  {df.shape[1]}")

print("\n📊 TIPOS DE DADOS:")
print(df.dtypes)

print("\n🔍 VALORES NULOS:")
print(df.isnull().sum())

print("\n📈 ESTATÍSTICAS DESCRITIVAS:")
print(df[["quantidade", "preco_unit", "total_venda"]].describe().round(2))


# ── Análise de Vendas ────────────────────────────────

# 1. Total faturado
total = df["total_venda"].sum()
print(f"\n💰 Faturamento Total: R$ {total:,.2f}")

# 2. Faturamento por categoria
print("\n📦 Faturamento por Categoria:")
cat_fat = (df.groupby("categoria")["total_venda"]
             .sum()
             .sort_values(ascending=False))
print(cat_fat)

# 3. Melhor vendedor
print("\n🏆 Ranking de Vendedores:")
vend_rank = (df.groupby("vendedor")["total_venda"]
               .sum()
               .sort_values(ascending=False))
print(vend_rank)

# 4. Produto mais vendido
print("\n📚 Top 3 Produtos (quantidade):")
top_prod = (df.groupby("produto")["quantidade"]
              .sum()
              .sort_values(ascending=False)
              .head(3))
print(top_prod)

# 5. Ticket médio por região
print("\n🗺️ Ticket médio por região:")
reg_media = (df.groupby("regiao")["total_venda"]
               .mean()
               .sort_values(ascending=False)
               .round(2))
print(reg_media)


# ── Visualizações ────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle("Dashboard: Livraria 2024", fontsize=14, fontweight="bold")

# Gráfico 1 — Categoria
ax1 = axes[0]
ax1.barh(cat_fat.index, cat_fat.values)
ax1.set_title("Faturamento por Categoria")

# Gráfico 2 — Vendedores
ax2 = axes[1]
ax2.bar(vend_rank.index, vend_rank.values)
ax2.set_title("Ranking de Vendedores")

# Gráfico 3 — Regiões
ax3 = axes[2]
reg_total = df.groupby("regiao")["total_venda"].sum()
ax3.pie(reg_total, labels=reg_total.index, autopct="%1.1f%%")
ax3.set_title("Participação por Região")

plt.tight_layout()
plt.show()

# ── Desafios Extras ──────────────────────────────────

# D1 — Evolução do faturamento mês a mês
df["data"] = pd.to_datetime(df["data"])
df["mes"] = df["data"].dt.month

faturamento_mes = df.groupby("mes")["total_venda"].sum()

print("\n📈 Evolução do faturamento mês a mês:")
print(faturamento_mes)


# D2 — Gráfico de linha mostrando a tendência de vendas
plt.figure()
plt.plot(faturamento_mes.index, faturamento_mes.values, marker="o")
plt.title("Tendência de vendas ao longo do tempo")
plt.xlabel("Mês")
plt.ylabel("Faturamento total")
plt.grid(True)
plt.show()


# D3 — Vendedor com o maior ticket médio
ticket_medio_vendedor = (
    df.groupby("vendedor")["total_venda"]
      .mean()
      .sort_values(ascending=False)
)

print("\n🏆 Vendedor com maior ticket médio:")
print(ticket_medio_vendedor.head(1))


# D4 — Filtrar vendas com total_venda > 200
vendas_altas = df[df["total_venda"] > 200]
categorias_vendas_altas = vendas_altas["categoria"].value_counts()

print("\n💎 Categorias que dominam as vendas acima de 200:")
print(categorias_vendas_altas)


# D5 — Adicionar 5 linhas com valores nulos e tratá-los
novas_linhas = pd.DataFrame([
    {
        "id_venda": 51,
        "data": "2024-07-01",
        "produto": None,
        "categoria": "Tecnologia",
        "quantidade": 2,
        "preco_unit": 89.90,
        "vendedor": "Ana Lima",
        "regiao": "Sudeste",
        "total_venda": None
    },
    {
        "id_venda": 52,
        "data": None,
        "produto": "Sapiens",
        "categoria": "Ciências",
        "quantidade": None,
        "preco_unit": 54.90,
        "vendedor": "Carlos Mendes",
        "regiao": "Sul",
        "total_venda": None
    },
    {
        "id_venda": 53,
        "data": "2024-07-03",
        "produto": "Clean Code",
        "categoria": None,
        "quantidade": 1,
        "preco_unit": None,
        "vendedor": "Bruno Costa",
        "regiao": "Nordeste",
        "total_venda": None
    },
    {
        "id_venda": 54,
        "data": "2024-07-04",
        "produto": "Cosmos",
        "categoria": "Ciências",
        "quantidade": 3,
        "preco_unit": 62.50,
        "vendedor": None,
        "regiao": "Norte",
        "total_venda": None
    },
    {
        "id_venda": 55,
        "data": "2024-07-05",
        "produto": "Atomic Habits",
        "categoria": "Autoajuda",
        "quantidade": None,
        "preco_unit": 44.90,
        "vendedor": "Fernanda Rocha",
        "regiao": None,
        "total_venda": None
    }
])

df_com_nulos = pd.concat([df, novas_linhas], ignore_index=True)

print("\n🔍 Valores nulos antes do tratamento:")
print(df_com_nulos.isnull().sum())

# Tratamento dos nulos
df_com_nulos["produto"] = df_com_nulos["produto"].fillna("Não informado")
df_com_nulos["categoria"] = df_com_nulos["categoria"].fillna("Não informada")
df_com_nulos["quantidade"] = df_com_nulos["quantidade"].fillna(df_com_nulos["quantidade"].mean())
df_com_nulos["preco_unit"] = df_com_nulos["preco_unit"].fillna(df_com_nulos["preco_unit"].mean())
df_com_nulos["vendedor"] = df_com_nulos["vendedor"].fillna("Não informado")
df_com_nulos["regiao"] = df_com_nulos["regiao"].fillna("Não informada")
df_com_nulos["data"] = df_com_nulos["data"].fillna("2024-07-02")

# Recalcula total_venda onde estiver nulo
df_com_nulos["total_venda"] = df_com_nulos["total_venda"].fillna(
    df_com_nulos["quantidade"] * df_com_nulos["preco_unit"]
)

print("\n✅ Valores nulos depois do tratamento:")
print(df_com_nulos.isnull().sum())
