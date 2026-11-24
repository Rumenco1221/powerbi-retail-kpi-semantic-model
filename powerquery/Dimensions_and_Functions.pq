// ===== Parámetro =====
// DataFolder = "C:\\Proyectos\\powerbi-retail-kpi-semantic-model\\data\\"   (Tipo: Texto)

// ===== fnLoadCsv — función reutilizable para cualquier dimensión =====
(fileName as text, types as list) as table =>
let
    Source  = Csv.Document(File.Contents(DataFolder & fileName), [Delimiter = ",", Encoding = 65001]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Typed   = Table.TransformColumnTypes(Headers, types, "en-US"),
    // Las columnas no tipadas llegan como texto: se limpian espacios en todas ellas
    TextCols = Table.ColumnsOfType(Typed, {type text}),
    Trimmed  = Table.TransformColumns(Typed, List.Transform(TextCols, (c) => {c, Text.Trim, type text}))
in
    Trimmed

// ===== Uso (una consulta por dimensión) =====
// DimStore    = fnLoadCsv("DimStore.csv",    {{"StoreKey", Int64.Type}})
// DimProduct  = fnLoadCsv("DimProduct.csv",  {{"ProductKey", Int64.Type}, {"ListPrice", Currency.Type}, {"UnitCost", Currency.Type}})
// DimCustomer = fnLoadCsv("DimCustomer.csv", {{"CustomerKey", Int64.Type}})
