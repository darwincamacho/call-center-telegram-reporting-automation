from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


OUTPUT_DIR = Path("outputs")
CHART_PATH = OUTPUT_DIR / "grafico_produccion_aplazaloh.png"


class ProductionReport:
    def __init__(self, data: pd.DataFrame) -> None:
        if data.empty:
            raise ValueError("El DataFrame de producción está vacío.")

        self.data = data.copy()
        self._prepare_data()

    def _prepare_data(self) -> None:
        required_columns = [
            "HORA",
            "MONTO_HORA",
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

        missing_columns = [
            column for column in required_columns if column not in self.data.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Faltan columnas requeridas en el DataFrame: {missing_columns}"
            )

        self.data["HORA_NUM"] = pd.to_numeric(
            self.data["HORA"], errors="coerce"
        ).fillna(0).astype(int)

        self.data["HORA_LABEL"] = self.data["HORA_NUM"].astype(str).str.zfill(2)

        numeric_columns = [
            "MONTO_HORA",
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

        for column in numeric_columns:
            self.data[column] = pd.to_numeric(
                self.data[column], errors="coerce"
            ).fillna(0)

        self.data = self.data[self.data["MONTO_HORA"] > 0]

        if self.data.empty:
            raise ValueError("No hay producción por hora mayor a cero.")

    def get_summary(self) -> dict:
        row = self.data.iloc[0]

        return {
            "total_b_mes": float(row["TOTAL_B_MES"]),
            "total_n_mes": float(row["TOTAL_N_MES"]),
            "total_dia": float(row["TOTAL_DIA"]),
            "total_n_dia": float(row["TOTAL_N_DIA"]),
            "cantidad_total_dia": int(row["CANTIDAD_TOTAL_DIA"]),
            "cantidad_flg2_dia": int(row["CANTIDAD_FLG2_DIA"]),
            "cantidad_flg6_dia": int(row["CANTIDAD_FLG6_DIA"]),
            "meta_dia": float(row["META_DIA"]),
            "cumplimiento_dia_pct": float(row["CUMPLIMIENTO_DIA_PCT"]),
        }

    @staticmethod
    def _format_k(value: float) -> str:
        return f"{value / 1000:.1f}K"

    @staticmethod
    def _format_money(value: float) -> str:
        return f"S/ {value:,.0f}"

    def create_chart(self) -> Path:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        fig, ax = plt.subplots(figsize=(10, 5))

        x_positions = list(range(len(self.data)))
        x_labels = self.data["HORA_LABEL"].tolist()

        bars = ax.bar(
            x_positions,
            self.data["MONTO_HORA"],
            width=0.42,
        )

        ax.set_xticks(x_positions)
        ax.set_xticklabels(x_labels)

        ax.set_title("VENTA POR HORA", fontsize=13, fontweight="bold", pad=18)
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.grid(False)

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

        ax.tick_params(axis="y", left=False, labelleft=False)
        ax.tick_params(axis="x", labelsize=10)

        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height * 0.96,
                self._format_k(height),
                ha="center",
                va="top",
                fontsize=9,
                fontweight="bold",
            )

        plt.tight_layout()
        plt.savefig(CHART_PATH, dpi=150)
        plt.close()

        return CHART_PATH

import numpy as np

MONTHLY_CHART_PATH = OUTPUT_DIR / "grafico_consolidado_mes.png"

class MonthlyConsolidatedReport:
    def __init__(self, data: pd.DataFrame) -> None:
        if data.empty:
            raise ValueError("El DataFrame del consolidado mensual está vacío.")

        self.data = data.copy()
        self._prepare_data()

    def _prepare_data(self) -> None:
        required_columns = ["FECHA", "TOTAL_DIA"]

        missing_columns = [
            column for column in required_columns if column not in self.data.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Faltan columnas requeridas en el DataFrame: {missing_columns}"
            )

        self.data["FECHA"] = pd.to_datetime(self.data["FECHA"])
        self.data["TOTAL_DIA"] = pd.to_numeric(
            self.data["TOTAL_DIA"], errors="coerce"
        ).fillna(0)

        self.data = self.data.sort_values("FECHA").reset_index(drop=True)

        self.data["LABEL"] = (
            self.data["FECHA"].dt.day.astype(str) + "-" + self.data["FECHA"].dt.strftime("%b")
        )

    @staticmethod
    def _format_k(value: float) -> str:
        return f"{value / 1000:.1f}K"

    def create_chart(self) -> Path:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        fig, ax = plt.subplots(figsize=(10, 5))

        x = np.arange(len(self.data))
        y = self.data["TOTAL_DIA"].to_numpy()

        ax.plot(x, y, linewidth=2.5, marker="o")

        ax.vlines(x, ymin=0, ymax=y, linewidth=1)

        if len(x) >= 2:
            coef = np.polyfit(x, y, 1)
            trend = np.poly1d(coef)
            ax.plot(x, trend(x), linestyle=":", linewidth=2)

        for xi, yi in zip(x, y):
            ax.text(
                xi,
                yi + (max(y) * 0.04),
                self._format_k(yi),
                ha="center",
                va="bottom",
                fontsize=10,
            )

        ax.set_xticks(x)
        ax.set_xticklabels(self.data["LABEL"], fontsize=10)

        ax.set_title("CONSOLIDADO MES", fontsize=13, fontweight="bold", pad=18)
        ax.set_xlabel("")
        ax.set_ylabel("")

        ax.tick_params(axis="y", left=False, labelleft=False)
        ax.grid(axis="y", linestyle="-", alpha=0.4)

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

        plt.tight_layout()
        plt.savefig(MONTHLY_CHART_PATH, dpi=150)
        plt.close()

        return MONTHLY_CHART_PATH
