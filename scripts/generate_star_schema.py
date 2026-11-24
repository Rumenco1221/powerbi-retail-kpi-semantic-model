"""Genera el modelo estrella (CSV) que consume Power BI: 1 tabla de hechos + 3 dimensiones.

La dimensión Fecha se crea en Power Query (powerquery/DimDate.pq), como en un proyecto real.
"""
import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

OUT = Path(__file__).resolve().parents[1] / "data"
OUT.mkdir(exist_ok=True)
rnd = random.Random(2026)

stores = pd.DataFrame([
    (1, "Palermo", "CABA", "Argentina", "Flagship"), (2, "Belgrano", "CABA", "Argentina", "Standard"),
    (3, "Córdoba Centro", "Centro", "Argentina", "Standard"), (4, "Rosario", "Litoral", "Argentina", "Standard"),
    (5, "Mendoza", "Cuyo", "Argentina", "Outlet"), (6, "Online", "Digital", "Argentina", "E-commerce"),
], columns=["StoreKey", "Store", "Region", "Country", "Format"])

categories = {"Tecnología": ["Notebook", "Monitor", "Tablet", "Auriculares", "Smartwatch"],
              "Hogar": ["Cafetera", "Aspiradora", "Lámpara", "Freidora de aire"],
              "Deportes": ["Bicicleta", "Zapatillas", "Mochila", "Yoga Mat"],
              "Moda": ["Campera", "Jean", "Remera", "Bolso"]}
rows, key = [], 1
for cat, items in categories.items():
    for it in items:
        price = round(rnd.uniform(15, 1400 if cat == "Tecnología" else 300), 2)
        rows.append((key, it, cat, price, round(price * rnd.uniform(0.45, 0.7), 2)))
        key += 1
products = pd.DataFrame(rows, columns=["ProductKey", "Product", "Category", "ListPrice", "UnitCost"])

customers = pd.DataFrame({
    "CustomerKey": range(1, 801),
    "Segment": [rnd.choice(["Consumidor", "Pyme", "Corporativo"]) for _ in range(800)],
    "AgeBand": [rnd.choice(["18-24", "25-34", "35-44", "45-54", "55+"]) for _ in range(800)],
})

sales, d = [], date(2024, 1, 1)
order = 1
while d <= date(2026, 10, 31):
    season = 1.6 if d.month in (11, 12) else 1.0
    growth = 1 + (d - date(2024, 1, 1)).days / 1500
    for _ in range(int(rnd.randint(8, 16) * season * growth)):
        p = products.sample(1, random_state=rnd.randint(0, 10**6)).iloc[0]
        qty = rnd.randint(1, 4)
        disc = rnd.choice([0, 0, 0, 0.05, 0.10, 0.15])
        sales.append((order, d.isoformat(), rnd.randint(1, 6), int(p.ProductKey), rnd.randint(1, 800), qty,
                      round(p.ListPrice * (1 - disc), 2), p.UnitCost, disc))
        order += 1
    d += timedelta(days=1)
fact = pd.DataFrame(sales, columns=["OrderID", "OrderDate", "StoreKey", "ProductKey", "CustomerKey", "Quantity",
                                    "UnitPrice", "UnitCost", "Discount"])

for name, df in {"FactSales": fact, "DimStore": stores, "DimProduct": products, "DimCustomer": customers}.items():
    df.to_csv(OUT / f"{name}.csv", index=False, encoding="utf-8")
    print(f"{name}: {len(df):,} filas")
