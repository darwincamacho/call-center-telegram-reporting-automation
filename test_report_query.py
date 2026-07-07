from database import SQLServerConnection
from queries import PRODUCCION_APLAZALOH_QUERY


def main() -> None:
    db = SQLServerConnection()
    df = db.read_query(PRODUCCION_APLAZALOH_QUERY)

    print(df)
    print("\nColumnas:")
    print(df.columns)

    print("\nResumen:")
    print(
        df[
            [
                "TOTAL_B_MES",
                "TOTAL_N_MES",
                "TOTAL_DIA",
                "TOTAL_N_DIA",
                "CANTIDAD_TOTAL_DIA",
                "CANTIDAD_FLG2_DIA",
                "CANTIDAD_FLG6_DIA",
                "META_DIA",
                "CUMPLIMIENTO_DIA_PCT",
            ]
        ].head(1)
    )


if __name__ == "__main__":
    main()
