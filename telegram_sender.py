import logging
import os
import time
from pathlib import Path
from typing import Callable

import requests
from dotenv import load_dotenv


load_dotenv()


RETRYABLE_REQUEST_ERRORS = (
    requests.exceptions.Timeout,
    requests.exceptions.ReadTimeout,
    requests.exceptions.ConnectionError,
)


class TelegramSender:
    def __init__(self) -> None:
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

        self._validate_env()

    def _validate_env(self) -> None:
        missing_vars = []

        if not self.bot_token:
            missing_vars.append("TELEGRAM_BOT_TOKEN")

        if not self.chat_id:
            missing_vars.append("TELEGRAM_CHAT_ID")

        if missing_vars:
            raise ValueError(
                f"Faltan variables de Telegram en el archivo .env: {', '.join(missing_vars)}"
            )

    def _post_with_retries(
        self,
        request_factory: Callable[[], requests.Response],
        operation_name: str,
        max_attempts: int = 3,
        wait_seconds: int = 5,
    ) -> None:
        for attempt in range(1, max_attempts + 1):
            try:
                response = request_factory()
                response.raise_for_status()
                return
            except RETRYABLE_REQUEST_ERRORS as error:
                logging.warning(
                    "Fallo temporal enviando %s a Telegram "
                    "(intento %s/%s): %s",
                    operation_name,
                    attempt,
                    max_attempts,
                    error,
                )

                if attempt == max_attempts:
                    raise

                time.sleep(wait_seconds)

    def send_message(self, message: str) -> None:
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

        def request_factory() -> requests.Response:
            return requests.post(
                url,
                data={
                    "chat_id": self.chat_id,
                    "text": message,
                    "parse_mode": "HTML",
                },
                timeout=(10, 60),
            )

        self._post_with_retries(request_factory, "mensaje")

    def send_photo(self, photo_path: Path, caption: str | None = None) -> None:
        if not photo_path.exists():
            raise FileNotFoundError(f"No existe el archivo: {photo_path}")

        url = f"https://api.telegram.org/bot{self.bot_token}/sendPhoto"

        def request_factory() -> requests.Response:
            with photo_path.open("rb") as photo_file:
                return requests.post(
                    url,
                    data={
                        "chat_id": self.chat_id,
                        "caption": caption or "",
                        "parse_mode": "HTML",
                    },
                    files={"photo": photo_file},
                    timeout=(10, 180),
                )

        self._post_with_retries(request_factory, "foto")
