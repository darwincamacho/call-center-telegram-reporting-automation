# Project Overview

## Objetivo

Automatizar la generación y distribución de un reporte de producción para la campaña Aplazaloh, combinando consultas a SQL Server, transformación con Python, visualización con Matplotlib y envío por Telegram.

## Flujo ETL / Reporting

1. Extract: lectura de datos desde SQL Server mediante SQLAlchemy y pyodbc.
2. Transform: limpieza de tipos, cálculo de totales, cumplimiento y preparación de etiquetas.
3. Load / Delivery: generación de imágenes en `outputs/` y envío del resumen a Telegram.
4. Observabilidad: registro de eventos y errores en `logs/`.

## Componentes Principales

- `database.py`: centraliza la conexión a SQL Server y valida variables obligatorias.
- `queries.py`: contiene las consultas SQL para producción diaria y consolidado mensual.
- `report.py`: prepara los DataFrames y genera gráficos.
- `telegram_sender.py`: encapsula el envío de mensajes y fotos con reintentos.
- `main.py`: coordina el flujo completo y controla la ventana de envío.

## Integración con Telegram

La distribución del reporte usa la Telegram Bot API. El bot token y el chat ID se configuran como variables de entorno (`TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHAT_ID`) para evitar credenciales hardcodeadas. El repositorio solo debe incluir `.env.example` como plantilla segura.

## Decisiones Técnicas

- Uso de `.env` para separar credenciales del código.
- Uso de SQL Server como fuente de verdad para los indicadores.
- Uso de pandas para normalizar tipos y calcular resúmenes.
- Uso de Matplotlib para gráficos exportables como imágenes.
- Uso de reintentos en Telegram para tolerar fallos temporales de red.
- Separación por módulos para facilitar mantenimiento y validación.

## Seguridad de Credenciales

Las credenciales de SQL Server y Telegram se cargan desde variables de entorno. El archivo `.env` real está excluido por `.gitignore` y no debe publicarse. El repositorio solo contiene `.env.example` con nombres de variables y valores vacíos o genéricos.

## Limitaciones

- La ejecución depende de conectividad con SQL Server.
- El envío depende de disponibilidad de la Telegram Bot API.
- Los scripts locales de scheduler pueden variar por máquina y no forman parte del repositorio público.
- Las consultas están acopladas a la estructura esperada de la tabla operativa.
