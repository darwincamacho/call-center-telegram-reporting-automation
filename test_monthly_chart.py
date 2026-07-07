from database import SQLServerConnection
from queries import CONSOLIDADO_MES_QUERY
from report import MonthlyConsolidatedReport


def main() -> None:
    db = SQLServerConnection()
    df = db.read_query(CONSOLIDADO_MES_QUERY)

    print(df)

    report = MonthlyConsolidatedReport(df)
    chart_path = report.create_chart()

    print("\nGráfico generado en:")
    print(chart_path)


if __name__ == "__main__":
    main()