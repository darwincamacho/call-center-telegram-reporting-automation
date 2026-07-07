# Aplazaloh Production Reporting Automation

Automatización en Python para generar y enviar un reporte operativo de producción de la campaña Aplazaloh. El proyecto consulta información desde SQL Server, genera indicadores diarios y mensuales, crea gráficos con Matplotlib y envía un resumen ejecutivo a Telegram.

Este repositorio está preparado como proyecto de portafolio para roles de Data Analyst, BI Analyst o Analytics Engineer Junior. Los datos, credenciales y endpoints reales no se incluyen por seguridad.

## Resumen Ejecutivo

El flujo automatiza una reportería recurrente que normalmente requeriría consultar la base de datos, consolidar métricas, generar gráficos y distribuir resultados manualmente. El resultado es un mensaje ejecutivo con métricas clave del día y del mes, acompañado por gráficos de producción por hora y consolidado mensual.

## Problema de Negocio

La operación necesita visibilidad frecuente sobre el avance de producción de la campaña:

- Seguimiento de venta por hora durante la jornada.
- Comparación contra una meta diaria.
- Consolidado mensual para observar tendencia.
- Distribución rápida de indicadores a responsables comerciales.

Sin automatización, este seguimiento puede consumir tiempo operativo y depender de tareas manuales repetitivas.

## Solución Implementada

La solución conecta a SQL Server mediante ODBC, ejecuta consultas parametrizadas por fecha actual, transforma los resultados con pandas, genera gráficos con Matplotlib y envía el reporte a Telegram. La ejecución local está pensada para integrarse con Windows Task Scheduler.

## Flujo del Proceso

1. Cargar variables de entorno desde `.env`.
2. Validar credenciales requeridas para SQL Server y Telegram.
3. Consultar producción diaria por hora.
4. Consultar consolidado mensual.
5. Calcular resumen ejecutivo: totales del mes, totales del día, meta y cumplimiento.
6. Generar gráficos en la carpeta `outputs/`.
7. Enviar mensaje y gráficos a Telegram.
8. Registrar eventos del proceso en `logs/`.

## Stack Tecnológico

- Python
- pandas
- SQLAlchemy
- pyodbc
- python-dotenv
- Matplotlib
- NumPy
- requests
- SQL Server
- Telegram Bot API
- Windows Task Scheduler

## Características Principales

- Conexión segura por variables de entorno.
- Consulta de producción diaria por hora.
- Consulta de consolidado mensual.
- Cálculo de meta diaria y cumplimiento.
- Generación automática de gráficos.
- Envío de mensaje ejecutivo a Telegram.
- Envío de gráficos como imágenes.
- Reintentos ante errores temporales de red en Telegram.
- Ventana de envío controlada por día y hora.
- Logging local para trazabilidad operativa.

## Arquitectura de Archivos

```text
.
├── database.py              # Conexión a SQL Server y lectura de queries
├── queries.py               # Consultas SQL del reporte diario y mensual
├── report.py                # Transformación de datos y generación de gráficos
├── telegram_sender.py       # Envío de mensajes y fotos a Telegram
├── main.py                  # Orquestación principal del flujo
├── test_connection.py       # Validación manual de conexión a SQL Server
├── test_report_query.py     # Validación manual de query principal
├── requirements.txt         # Dependencias del proyecto
├── .env.example             # Plantilla de variables de entorno
├── .gitignore               # Exclusiones para Git
└── docs/
    └── PROJECT_OVERVIEW.md  # Documentación técnica breve
```

Las carpetas `logs/`, `outputs/`, entornos virtuales, cachés de Python y archivos locales del scheduler se excluyen del repositorio.

## Ejemplo de Salida en Telegram

```text
REPORTE PRODUCCIÓN APLAZALOH

Total B Mes: S/ 1,250,000.00
Total N Mes: S/ 1,120,000.00
Total Día: S/ 85,000.00
Total N Día: S/ 78,500.00
Meta Día: S/ 260,869.57
Cumplimiento Día: 30.09%

Cantidad Vendida Día
Total: 120
FLG2: 75
FLG6: 45
```

Los valores anteriores son ilustrativos y no representan datos reales.

## Instalación

Crear y activar un entorno virtual:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Además, el equipo debe tener instalado un driver compatible de SQL Server, por ejemplo `ODBC Driver 18 for SQL Server`.

## Configuración

Crear un archivo `.env` local a partir de `.env.example`:

```bash
copy .env.example .env
```

Completar las variables requeridas:

```env
SQL_SERVER=
SQL_DATABASE=
SQL_USERNAME=
SQL_PASSWORD=
SQL_DRIVER=ODBC Driver 18 for SQL Server

TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

El archivo `.env` contiene credenciales y no debe subirse al repositorio.

## Telegram Bot Setup

Para habilitar el envío del reporte por Telegram:

1. Abrir Telegram y buscar el bot oficial `BotFather`.
2. Crear un nuevo bot con el comando `/newbot`.
3. Copiar el token generado por BotFather y guardarlo como `TELEGRAM_BOT_TOKEN` en el archivo `.env` local.
4. Usar un chat privado con el bot o crear un grupo para recibir los reportes.
5. Si se usa un grupo, agregar el bot al grupo.
6. Obtener el `TELEGRAM_CHAT_ID` del chat o grupo donde se enviarán los mensajes.
7. Guardar ambos valores en `.env`, tomando `.env.example` como referencia.

Ejemplo seguro:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

Notas de seguridad:

- Nunca subir `.env` a GitHub.
- Mantener `.env.example` sin credenciales reales.
- Si un token fue expuesto accidentalmente, regenerarlo desde BotFather y reemplazarlo en el entorno local.

## Ejecución Manual

Ejecutar el flujo principal:

```bash
python main.py
```

El script valida una ventana de envío antes de generar y enviar el reporte.

## Validar Conexión

Para probar la conexión con SQL Server:

```bash
python test_connection.py
```

Esta prueba requiere que el archivo `.env` local esté configurado correctamente.

## Automatización

El proyecto puede ejecutarse con Windows Task Scheduler usando un script local que active el entorno de Python y llame a `python main.py`.

Recomendaciones:

- Mantener rutas locales y nombres de usuario fuera del repositorio.
- No incluir tokens, contraseñas ni identificadores de chat en scripts.
- Configurar la frecuencia de ejecución según la necesidad operativa.
- Revisar los logs locales si una ejecución programada falla.

## Business Impact

- Automatiza una reportería recurrente y reduce trabajo manual.
- Permite monitoreo oportuno de producción durante la jornada.
- Mejora la visibilidad comercial por hora y por mes.
- Estandariza el formato del reporte enviado a usuarios de negocio.
- Reduce dependencia de consultas manuales y generación manual de gráficos.

## Disclaimer

Este repositorio no incluye datos internos, credenciales, tokens, chat IDs, endpoints privados ni salidas reales de producción. Las variables sensibles deben configurarse solo en un archivo `.env` local, excluido por `.gitignore`.
