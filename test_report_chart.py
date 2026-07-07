from database import SQLServerConnection
from queries import PRODUCCION_APLAZALOH_QUERY
from report import ProductionReport


def main() -> None:
    db = SQLServerConnection()
    df = db.read_query(PRODUCCION_APLAZALOH_QUERY)

    report = ProductionReport(df)

    summary = report.get_summary()
    chart_path = report.create_chart()

    print("Resumen:")
    print(summary)

    print("\nGráfico generado en:")
    print(chart_path)


if __name__ == "__main__":
    main()