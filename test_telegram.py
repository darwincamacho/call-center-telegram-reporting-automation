from telegram_sender import TelegramSender


def main() -> None:
    sender = TelegramSender()
    sender.send_message("Prueba OK: reporte Aplazaloh conectado a Telegram.")


if __name__ == "__main__":
    main()