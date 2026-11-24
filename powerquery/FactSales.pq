// FactSales — Carga parametrizada, tipado explícito y columnas calculadas en origen
// Requiere el parámetro DataFolder (texto) con la ruta a la carpeta /data del repositorio.
let
    Source     = Csv.Document(File.Contents(DataFolder & "FactSales.csv"),
                    [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Headers    = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed      = Table.TransformColumnTypes(Headers, {
                    {"OrderID", Int64.Type}, {"OrderDate", type date}, {"StoreKey", Int64.Type},
                    {"ProductKey", Int64.Type}, {"CustomerKey", Int64.Type}, {"Quantity", Int64.Type},
                    {"UnitPrice", Currency.Type}, {"UnitCost", Currency.Type}, {"Discount", Percentage.Type}},
                    "en-US"),
    NoErrors   = Table.RemoveRowsWithErrors(Typed),
    // Calcular importes en Power Query (no en DAX) mejora compresión y rendimiento del modelo
    AddSales   = Table.AddColumn(NoErrors, "SalesAmount", each [Quantity] * [UnitPrice], Currency.Type),
    AddCost    = Table.AddColumn(AddSales, "CostAmount", each [Quantity] * [UnitCost], Currency.Type)
in
    AddCost
