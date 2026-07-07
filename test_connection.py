from database import SQLServerConnection


query = """
SELECT TOP 5 *
FROM ZRP_PRODUCCION_GESTOR_OH_APLAZALOH;
"""


def main() -> None:
    db = SQLServerConnection()
    df = db.read_query(query)

    print(f"Driver activo: {db.driver}")
    print(f"Conexión OK. Filas recuperadas: {len(df)}")
    print(df.columns)


if __name__ == "__main__":
    main()
