LAYA - Motor de Decisiones Empresarial & Exposición Financiera

LAYA es una plataforma interactiva de automatización avanzada y toma de decisiones multi-rubro orientada a la gestión de riesgos empresariales y análisis predictivo. Permite evaluar comentarios, solicitudes o reclamos en tiempo real mediante modelos de clasificación, análisis de sentimiento y evaluación de riesgos críticos, calculando la exposición financiera asociada de forma automática.

Características Principales

Ingreso Multiformato de Datos: Procesamiento masivo desde archivos (CSV, XLSX, TXT) o entrada manual directo en la interfaz.

Procesamiento Concurrente: Evaluación acelerada mediante multithreading (ThreadPoolExecutor) para optimizar tiempos en grandes volúmenes de datos.

Rubros Dinámicos y Personalizados: Adaptabilidad a distintas industrias (Soporte, Ventas, Reclamos, etc.) con la opción de crear y guardar rubros customizados en tiempo de ejecución.

Evaluación Multi-Criterio con LAYA Router:

Categorización (Choice): Asignación inteligente de área o categoría, con sistema de fallback automático por palabras clave (keywords).

Análisis de Sentimiento (Score): Calificación del tono del texto (negativo, neutral, positivo).

Criticidad y Riesgo (Noul): Estimación de probabilidad de riesgo alto o urgencia.

Matriz de Exposición Financiera: Cálculo dinámico de la pérdida/riesgo total y crítico en función del impacto unitario configurado.

Briefing Ejecutivo Automatizado: Resumen con diagnósticos operativos clave e indicadores financieros priorizados.

Persistencia Relacional (SQLite): Guardado automático del historial de evaluaciones (laya_history.db) con herramientas de filtrado y visualización de tendencias acumuladas.

Exportación de Resultados: Descarga directa de informes en formatos .csv y .xlsx.

Requisitos Previos e Instalación

1. Clonar el repositorio

git clone [https://github.com/wgekko/automatizacion-toma-decisiones.git](https://github.com/wgekko/automatizacion-toma-decisiones.git)
cd automatizacion-toma-decisiones

2. Crear un entorno virtual (Recomendado)

# En Linux/macOS
python -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
venv\Scripts\activate

3. Instalar dependencias

Instala los paquetes necesarios indicados en requirements.txt:

pip install -r requirements.txt


Estructura del Proyecto

.
├── main.py                    # Aplicación principal de Streamlit
├── requirements.txt           # Dependencias del sistema
├── components/
│   └── rubros_config.py       # Configuración base de rubros e industrias
├── laya_history.db            # Base de datos SQLite (se genera automáticamente)
├── laya_audit.log             # Registro de auditoría y logs del sistema
└── README.md                  # Documentación del proyecto

para mantener los estilos y fondos de esta app se debe crear una carpeta .streamlit y dentro de ella generar 
un archivo llamado config.toml
"
[server]
enableStaticServing = true

[[theme.fontFaces]]
family = "Inter"
url = "app/static/Inter_18pt-Regular.ttf"
style = "normal"
weight = 400

[[theme.fontFaces]]
family = "Inter"
url = "app/static/Inter_18pt-Medium.ttf"
style = "normal"
weight = 500

[[theme.fontFaces]]
family = "Inter"
url = "app/static/Inter_18pt-SemiBold.ttf"
style = "normal"
weight = 600

[[theme.fontFaces]]
family = "Inter"
url = "app/static/Inter_18pt-Bold.ttf"
style = "normal"
weight = 700

[[theme.fontFaces]]
family = "JetBrainsMono"
url = "app/static/JetBrainsMono-Regular.ttf"
style = "normal"
weight = 400

[[theme.fontFaces]]
family = "JetBrainsMono"
url = "app/static/JetBrainsMono-Medium.ttf"
style = "normal"
weight = 500

[[theme.fontFaces]]
family = "JetBrainsMono"
url = "app/static/JetBrainsMono-Bold.ttf"
style = "normal"
weight = 700

[theme]
# 🌙 DARK MODE DEVELOPER PALETTE 🌙
primaryColor = "#a855f7"             # Purple-500 - vibrant, code-like accent
backgroundColor = "#0d1117"          # GitHub-like dark background - developer comfort
secondaryBackgroundColor = "#161b22" # Slightly lighter - cards and sections
textColor = "#f0f6fc"                # Light blue-white - easy on eyes
linkColor = "#58a6ff"                # GitHub-like blue - familiar developer color
borderColor = "#30363d"              # Dark gray borders - subtle definition
showWidgetBorder = true
baseRadius = "0.375rem"              # Moderate rounding - modern feel
font = "Inter"                       # Inter - clean, developer-friendly
headingFont = "Inter"                # Consistent hierarchy
codeFont = "JetBrainsMono"           # JetBrains Mono - popular with developers
codeBackgroundColor = "#21262d"      # Darker code background - clear distinction
showSidebarBorder = true

[theme.sidebar]
backgroundColor = "#161b22"          # Darker sidebar - VS Code style
secondaryBackgroundColor = "#21262d" # Code-like sections
"


Configuración y Uso

Ejecutar la Aplicación

Para iniciar el panel de control interactivo con Streamlit, ejecuta:

streamlit run main.py


Panel Lateral de Configuración (Sidebar)

Selección de Rubro / Industria: Elige un rubro precargado o define uno nuevo con sus propias categorías, instrucciones y valores económicos.

Idioma del Motor: Selecciona entre automático, English o Multilingual.

Impacto Económico Unitario ($): Ajusta el valor financiero base de referencia por evento.

Umbral de Alerta Crítica (%): Define el porcentaje límite para marcar un caso como criticidad alta.

Pre-cargar Modelos: Habilita la persistencia del modelo LAYA en memoria para acelerar subsiguientes inferencias.

🔍 Registro de Auditoría (Logging)

El sistema genera de forma continua un archivo de log estructurado laya_audit.log que registra:

Eventos de carga del Router LAYA.

Activaciones del mecanismo de fallback de palabras clave.

Excepciones y errores durante la evaluación de registros.

Exportación y Reportes

Tanto en la pestaña de Evaluación Activa como en el Histórico (SQLite), la aplicación permite exportar los datos analizados a Excel (.xlsx) y CSV (.csv) con métricas ponderadas por nivel de riesgo y severidad.


video demo 



https://github.com/user-attachments/assets/a9f0fb3d-669e-48b5-a2c3-381c12c53bf5


