# Guía de construcción en Power BI Desktop

## 1. Parámetro
**Inicio › Transformar datos › Administrar parámetros › Nuevo**
- Nombre: `DataFolder` · Tipo: Texto · Valor: ruta a `/data` terminada en `\` (ej. `C:\Proyectos\powerbi-retail-kpi-semantic-model\data\`).

## 2. Consultas (Power Query)
Para cada archivo de `powerquery/`: **Nuevo origen › Consulta en blanco › Editor avanzado**, pegar y renombrar.
1. `fnLoadCsv` (la función del archivo `Dimensions_and_Functions.pq`).
2. `DimStore`, `DimProduct`, `DimCustomer` invocando la función (ver comentarios del archivo).
3. `FactSales` (`FactSales.pq`).
4. `DimDate` (`DimDate.pq`) — depende de `FactSales`.
5. **Cerrar y aplicar.**

## 3. Modelo
Vista de modelo → crear relaciones (cardinalidad 1:*, dirección de filtro **única**):

| Desde (1) | Hacia (*) |
|---|---|
| `DimDate[Date]` | `FactSales[OrderDate]` |
| `DimProduct[ProductKey]` | `FactSales[ProductKey]` |
| `DimStore[StoreKey]` | `FactSales[StoreKey]` |
| `DimCustomer[CustomerKey]` | `FactSales[CustomerKey]` |

- `DimDate` › **Marcar como tabla de fechas** › columna `Date`.
- Ordenar `MonthName` por `MonthNumber`.
- Ocultar claves y columnas técnicas de `FactSales` en la vista de informe.

## 4. Medidas
**Introducir datos** → tabla vacía `_Measures`. Pegar cada medida de `dax/Measures.dax` (Nueva medida). Formatos:
- `%` → Porcentaje, 1 decimal · importes → Moneda, 0 decimales.
- Asignar *carpeta de visualización* según el comentario de sección.

## 5. Tema
**Vista › Temas › Examinar temas** → `theme/estela_corporate_theme.json`.

## 6. Diseño sugerido (1 página, 16:9)
- Fila superior: 4 tarjetas — `Sales YTD`, `YoY Arrow` (color con formato condicional = `YoY Color`), `Gross Margin %`, `Average Ticket`.
- Izquierda: gráfico de líneas `Sales` y `Sales PY` por `MonthShort`.
- Derecha: barras por `Category` y por `Store`.
- Segmentadores: `Year`, `Region`. Título del informe = medida `Title Sales`.

## 7. Validación
Filtrar Año = 2026 y meses 1–10, y comparar con `docs/EXPECTED_VALUES.md`. Si coinciden, el modelo está correcto.

## 8. Guardar para Git
**Archivo › Guardar como › Proyecto de Power BI (.pbip)**: guarda el informe y el modelo como archivos de texto, ideales para versionar en GitHub.
