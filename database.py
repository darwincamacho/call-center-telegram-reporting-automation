import os
from urllib.parse import quote_plus

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv(override=True)


class SQLServerConnection:
    def __init__(self) -> None:
        self.server = os.getenv("SQL_SERVER")
        self.database = os.getenv("SQL_DATABASE")
        self.username = os.getenv("SQL_USERNAME")
        self.password = os.getenv("SQL_PASSWORD")
        self.driver = os.getenv("SQL_DRIVER", "ODBC Driver 18 for SQL Server")

        self._validate_env()

    def _validate_env(self) -> None:
        required_vars = {
            "SQL_SERVER": self.server,
            "SQL_DATABASE": self.database,
            "SQL_USERNAME": self.username,
            "SQL_PASSWORD": self.password,
            "SQL_DRIVER": self.driver,
        }

        missing_vars = [key for key, value in required_vars.items() if not value]

        if missing_vars:
            raise ValueError(
                f"Faltan variables en el archivo .env: {', '.join(missing_vars)}"
            )

    def get_engine(self):
        connection_string = (
            f"DRIVER={{{self.driver}}};"
            f"SERVER={self.server};"
            f"DATABASE={self.database};"
            f"UID={self.username};"
            f"PWD={self.password};"
            "Encrypt=yes;"
            "TrustServerCertificate=yes;"
        )

        params = quote_plus(connection_string)

        return create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

    def read_query(self, query: str) -> pd.DataFrame:
        engine = self.get_engine()

        with engine.connect() as connection:
            return pd.read_sql(query, connection)
