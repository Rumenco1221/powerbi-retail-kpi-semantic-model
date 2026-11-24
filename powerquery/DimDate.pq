// DimDate — Tabla calendario dinámica (se ajusta sola al rango de FactSales)
// Pegar en Power Query: Inicio > Nuevo origen > Consulta en blanco > Editor avanzado
let
    MinDate   = Date.StartOfYear(List.Min(FactSales[OrderDate])),
    MaxDate   = Date.EndOfYear(List.Max(FactSales[OrderDate])),
    DayCount  = Duration.Days(MaxDate - MinDate) + 1,
    Dates     = List.Dates(MinDate, DayCount, #duration(1, 0, 0, 0)),
    AsTable   = Table.FromList(Dates, Splitter.SplitByNothing(), {"Date"}),
    Typed     = Table.TransformColumnTypes(AsTable, {{"Date", type date}}),
    AddCols   = Table.AddColumn(Typed, "Attrs", each [
                    Year        = Date.Year([Date]),
                    MonthNumber = Date.Month([Date]),
                    MonthName   = Text.Proper(Date.MonthName([Date], "es-AR")),
                    MonthShort  = Text.Start(Text.Proper(Date.MonthName([Date], "es-AR")), 3),
                    YearMonth   = Date.Year([Date]) * 100 + Date.Month([Date]),
                    Quarter     = "T" & Text.From(Date.QuarterOfYear([Date])),
                    WeekDayNum  = Date.DayOfWeek([Date], Day.Monday) + 1,
                    WeekDay     = Text.Proper(Date.DayOfWeekName([Date], "es-AR")),
                    IsWeekend   = Date.DayOfWeek([Date], Day.Monday) >= 5
                ]),
    Expanded  = Table.ExpandRecordColumn(AddCols, "Attrs",
                    {"Year","MonthNumber","MonthName","MonthShort","YearMonth","Quarter","WeekDayNum","WeekDay","IsWeekend"}),
    Final     = Table.TransformColumnTypes(Expanded, {
                    {"Year", Int64.Type}, {"MonthNumber", Int64.Type}, {"YearMonth", Int64.Type},
                    {"WeekDayNum", Int64.Type}, {"IsWeekend", type logical}})
in
    Final
