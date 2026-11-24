"""Calcula en pandas los valores que deben devolver las medidas DAX (para validar el modelo) y dibuja el mockup."""
from pathlib import Path
import pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

D = Path(__file__).resolve().parents[1] / "data"
f = pd.read_csv(D / "FactSales.csv", parse_dates=["OrderDate"])
p = pd.read_csv(D / "DimProduct.csv"); s = pd.read_csv(D / "DimStore.csv")
f["Sales"] = f.Quantity * f.UnitPrice; f["Cost"] = f.Quantity * f.UnitCost
f = f.merge(p[["ProductKey", "Category"]], on="ProductKey").merge(s[["StoreKey", "Store"]], on="StoreKey")
ytd = lambda y: f[(f.OrderDate.dt.year == y) & (f.OrderDate.dt.month <= 10)]
cur, prev = ytd(2026), ytd(2025)
kpi = {
    "Sales YTD 2026 (ene-oct)": cur.Sales.sum(),
    "Sales PY YTD (ene-oct 2025)": prev.Sales.sum(),
    "YoY %": cur.Sales.sum() / prev.Sales.sum() - 1,
    "Gross Margin % 2026": 1 - cur.Cost.sum() / cur.Sales.sum(),
    "Orders 2026": cur.OrderID.nunique(),
    "Average Ticket 2026": cur.Sales.sum() / cur.OrderID.nunique(),
}
lines = ["| Medida | Valor esperado |", "|---|---|"]
for k, v in kpi.items():
    lines.append(f"| {k} | {v:.1%} |" if "%" in k else f"| {k} | {v:,.2f} |")
(Path(__file__).resolve().parents[1] / "docs" / "EXPECTED_VALUES.md").write_text(
    "# Valores esperados para validar las medidas DAX\n\nFiltro: año 2026, meses enero a octubre.\n\n" + "\n".join(lines) + "\n", encoding="utf-8")

# Mockup del tablero
fig = plt.figure(figsize=(14, 8), facecolor="#F3F4F6")
fig.text(0.03, 0.95, "Retail KPI Dashboard · 2026 YTD", fontsize=18, fontweight="bold", color="#111827")
fig.text(0.03, 0.915, "Mockup generado con los mismos datos del modelo · Tema: Estela Oviedo Corporate", fontsize=10, color="#6B7280")
cards = [("Ventas YTD", f"$ {kpi['Sales YTD 2026 (ene-oct)']/1e6:,.2f} M"), ("vs año anterior", f"{kpi['YoY %']:+.1%}"),
         ("Margen bruto", f"{kpi['Gross Margin % 2026']:.1%}"), ("Ticket promedio", f"$ {kpi['Average Ticket 2026']:,.0f}")]
for i, (t, v) in enumerate(cards):
    ax = fig.add_axes([0.03 + i * 0.24, 0.74, 0.22, 0.14]); ax.set_xticks([]); ax.set_yticks([])
    ax.set_facecolor("white"); [sp.set_color("#E5E7EB") for sp in ax.spines.values()]
    ax.text(0.06, 0.68, t, fontsize=11, color="#4B5563", transform=ax.transAxes)
    ax.text(0.06, 0.22, v, fontsize=22, fontweight="bold", color="#16A34A" if "+" in v else "#1E3A8A", transform=ax.transAxes)
m = f.groupby([f.OrderDate.dt.year.rename("Y"), f.OrderDate.dt.month.rename("M")]).Sales.sum().unstack(0)
ax = fig.add_axes([0.04, 0.08, 0.5, 0.58]); ax.set_facecolor("white")
ax.plot(m.index, m[2026] / 1e3, color="#1E3A8A", lw=2.5, marker="o", label="2026")
ax.plot(m.index, m[2025] / 1e3, color="#94A3B8", lw=2, ls="--", label="2025 (PY)")
ax.set_xticks(range(1, 13), ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"])
ax.set_title("Ventas mensuales vs año anterior (miles $)", loc="left", fontweight="bold"); ax.legend(frameon=False)
ax.spines[["top", "right"]].set_visible(False)
c = cur.groupby("Category").Sales.sum().sort_values()
ax = fig.add_axes([0.62, 0.42, 0.35, 0.24]); ax.barh(c.index, c / 1e3, color="#2563EB")
ax.set_title("Ventas por categoría (miles $)", loc="left", fontweight="bold"); ax.spines[["top", "right"]].set_visible(False)
st = cur.groupby("Store").Sales.sum().sort_values()
ax = fig.add_axes([0.62, 0.08, 0.35, 0.26]); ax.barh(st.index, st / 1e3, color="#0EA5E9")
ax.set_title("Ventas por tienda (miles $)", loc="left", fontweight="bold"); ax.spines[["top", "right"]].set_visible(False)
fig.savefig(Path(__file__).resolve().parents[1] / "docs" / "dashboard_mockup.png", dpi=110, facecolor=fig.get_facecolor())
print(kpi)
