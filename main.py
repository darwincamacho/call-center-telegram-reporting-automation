import logging
from pathlib import Path

from database import SQLServerConnection
from queries import PRODUCCION_APLAZALOH_QUERY, CONSOLIDADO_MES_QUERY
from report import ProductionReport, MonthlyConsolidatedReport
from telegram_sender import TelegramSender
from datetime import datetime, time 


LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "app.log"


def setup_logging() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        encoding="utf-8",
    )


def build_telegram_message(summary: dict) -> str:
    return (
        "<b>REPORTE PRODUCCIÓN APLAZALOH</b>\n\n"
        f"<b>Total B Mes:</b> S/ {summary['total_b_mes']:,.2f}\n"
        f"<b>Total N Mes:</b> S/ {summary['total_n_mes']:,.2f}\n"
        f"<b>Total Día:</b> S/ {summary['total_dia']:,.2f}\n"
        f"<b>Total N Día:</b> S/ {summary['total_n_dia']:,.2f}\n"
        f"<b>Meta Día:</b> S/ {summary['meta_dia']:,.2f}\n"
        f"<b>Cumplimiento Día:</b> {summary['cumplimiento_dia_pct']:.2f}%\n\n"
        "<b>📦 Cantidad Vendida Día</b>\n"
        f"• <b>Total:</b> {summary['cantidad_total_dia']:,}\n"
        f"• <b>FLG2:</b> {summary['cantidad_flg2_dia']:,}\n"
        f"• <b>FLG6:</b> {summary['cantidad_flg6_dia']:,}"
    )

def should_send_report(now: datetime) -> bool:
    if now.weekday() == 6:
        return False

    if not (time(9, 0) <= now.time() <= time(20, 0)):
        return False

    if now.minute not in (0, 30):
        return False

    return True

def main() -> None:
    setup_logging()

    now = datetime.now()

    if not should_send_report(now):
        logging.info(
            "Ejecución fuera de ventana permitida. No se envía reporte. Fecha/hora: %s",
            now.strftime("%Y-%m-%d %H:%M:%S"),
        )
        print("Ejecución fuera de ventana permitida. No se envía reporte.")
        return

    logging.info("Iniciando generación de reporte Aplazaloh.")

    try:
        db = SQLServerConnection()

        logging.info("Ejecutando query de producción por hora.")
        df_hourly = db.read_query(PRODUCCION_APLAZALOH_QUERY)

        hourly_report = ProductionReport(df_hourly)
        hourly_chart_path = hourly_report.create_chart()
        hourly_summary = hourly_report.get_summary()

        logging.info("Gráfico de producción por hora generado: %s", hourly_chart_path)
        logging.info("Resumen horario: %s", hourly_summary)

        logging.info("Ejecutando query de consolidado mensual.")
        df_monthly = db.read_query(CONSOLIDADO_MES_QUERY)

        monthly_report = MonthlyConsolidatedReport(df_monthly)
        monthly_chart_path = monthly_report.create_chart()

        logging.info("Gráfico consolidado mensual generado: %s", monthly_chart_path)

        telegram = TelegramSender()
        telegram_message = build_telegram_message(hourly_summary)

        logging.info("Enviando mensaje ejecutivo a Telegram.")
        telegram.send_message(telegram_message)

        logging.info("Enviando gráfico de producción por hora a Telegram.")
        telegram.send_photo(
            hourly_chart_path,
            caption="Venta por hora - Aplazaloh",
        )

        logging.info("Enviando gráfico consolidado mensual a Telegram.")
        telegram.send_photo(
            monthly_chart_path,
            caption="Consolidado mes - Aplazaloh",
        )

        print("Reporte generado y enviado correctamente.")
        print(f"Gráfico venta por hora: {hourly_chart_path}")
        print(f"Gráfico consolidado mes: {monthly_chart_path}")
        print("Resumen:")
        print(hourly_summary)

        logging.info("Proceso finalizado correctamente.")

    except Exception as error:
        logging.exception("Error durante la generación/envío del reporte: %s", error)
        raise


if __name__ == "__main__":
    main()
