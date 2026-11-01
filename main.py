# ==========================================
# IMPORTACIÓN DE LIBRERÍAS Y SILENCIADO DE LOGS
# ==========================================
import concurrent.futures
from datetime import datetime
import io
import json
import logging
import sqlite3
from components.rubros_config import BASE_RUBROS_CONFIG
import warnings

import laya
import pandas as pd
import streamlit as st

# 1. Silenciar el sistema de warnings estándar de Python
warnings.filterwarnings(
    action="ignore",
    message=".*Accessing `__path__` from.*",
    category=UserWarning,
)

# 2. Silenciar los logs internos de la librería transformers en consola
logging.getLogger("transformers").setLevel(logging.ERROR)

# Configuración de Logging Estructurado y Auditoría
logging.basicConfig(
    filename="laya_audit.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8",
)

st.set_page_config(
    page_title="LAYA - automatización avanzada - Toma de Decisiones Multi-Rubro ",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "LAYA Avanzado - Toma de decisiones multi-rubro"
    },
)

# ==========================================
# HELPER PARA EXPORTACIÓN DE ARCHIVOS EXCEL
# ==========================================
def to_excel(df: pd.DataFrame) -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Evaluacion_LAYA")
    return output.getvalue()

# ==========================================
# BASE DE DATOS SQLITE (Persistencia Relacional)
# ==========================================
DB_FILE = "laya_history.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS evaluacion_historica (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            rubro TEXT,
            comentario TEXT,
            categoria TEXT,
            sentimiento TEXT,
            prob_riesgo REAL,
            impacto_financiero REAL,
            modelo_routing TEXT
        )
    """)
    conn.commit()
    conn.close()


init_db()


def guardar_evaluaciones_db(df_eval, rubro):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for _, row in df_eval.iterrows():
        c.execute(
            """
            INSERT INTO evaluacion_historica 
            (timestamp, rubro, comentario, categoria, sentimiento, prob_riesgo, impacto_financiero, modelo_routing)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                now_str,
                rubro,
                str(row["comment"]),
                str(row["choice_answer"]),
                str(row["score_answer"]),
                float(row["noul_answer"]),
                float(row["financial_impact"]),
                str(row["routing_model"]),
            ),
        )
    conn.commit()
    conn.close()

# Session State para Persistencia de Rubros Personalizados
if "custom_rubros" not in st.session_state:
    st.session_state.custom_rubros = {}

RUBROS_CONFIG = {**BASE_RUBROS_CONFIG, **st.session_state.custom_rubros}

# ==========================================
# BARRA LATERAL (Configuración Completa & Rubros Dinámicos)
# ==========================================
st.sidebar.subheader(":material/settings: Parámetros del Sistema")

selected_rubro_name = st.sidebar.selectbox(
    "Selecciona Rubro / Industria:",
    options=list(RUBROS_CONFIG.keys()),
    help="Elige la industria para adaptar automáticamente los criterios de LAYA.",
)
current_config = RUBROS_CONFIG[selected_rubro_name]

lang_option = st.sidebar.radio(
    "Idioma del Motor LAYA:",
    options=["automático", "English", "Multilingual"],
    index=0,
    help=(
        "• Automático: LAYA detecta el idioma\n• English: Optimizado en"
        " inglés\n• Multilingual: 100+ idiomas"
    ),
)

st.sidebar.subheader("Matriz Financiera")
unit_financial_value = st.sidebar.number_input(
    current_config.get("financial_label", "Impacto Económico Unitario ($)"),
    min_value=1000.0,
    max_value=100000000.0,
    value=current_config.get("default_val", 100000.0),
    step=10000.0,
    help=(
        "Monto de referencia utilizado para calcular la Exposición Financiera"
        " Esperada ($) por registro."
    ),
)

threshold_value = (
    st.sidebar.slider(
        "Umbral de Alerta Critica (%):",
        min_value=5,
        max_value=95,
        value=40,
        help="Porcentaje mínimo de probabilidad para activar alerta crítica",
    )
    / 100.0
)

# Creador Dinámico de Rubros
with st.sidebar.expander(":material/rubric: Crear Rubro Personalizado"):
    with st.form("new_rubro_form"):
        nuevo_nombre = st.text_input("Nombre del Rubro")
        nueva_desc = st.text_input("Descripción breve")
        nuevo_placeholder = st.text_area("Texto de ejemplo (Placeholder)")

        st.markdown("**Configuración Categoría Principal (Choice):**")
        c_name = st.text_input("Clave categoría (ej: area)", value="area")
        c_inst = st.text_input(
            "Instrucción evaluativa", value="Qué área gestiona esto?"
        )
        c_opts = st.text_input(
            "Opciones separadas por coma", value="soporte, ventas, reclamos"
        )

        submitted_rubro = st.form_submit_button("Guardar Rubro Dinámico")
        if submitted_rubro and nuevo_nombre:
            opts_dict = {
                o.strip(): f"asuntos relacionados con {o.strip()}"
                for o in c_opts.split(",")
            }
            if "other" not in opts_dict:
                opts_dict["other"] = "everything else"

            st.session_state.custom_rubros[nuevo_nombre] = {
                "description": nueva_desc,
                "placeholder": nuevo_placeholder,
                "questions": {
                    c_name: {
                        "type": "choice",
                        "instructions": c_inst,
                        "criteria": opts_dict,
                    },
                    "sentiment": {
                        "type": "score",
                        "instructions": "Cuál es el sentimiento?",
                        "criteria": ["negativo", "neutral", "positivo"],
                    },
                    "critical_risk": {
                        "type": "noul",
                        "instructions": (
                            "¿El mensaje representa un riesgo crítico o urgencia alta?"
                        ),
                    },
                },
                "keywords": {
                    k.strip(): [k.strip()]
                    for k in c_opts.split(",")
                    if k.strip() != "other"
                },
                "metric_labels": (
                    c_name.capitalize(),
                    "Sentimiento",
                    "Riesgo Crítico",
                ),
                "financial_label": f"Impacto Unitario Estimado para {nuevo_nombre} ($)",
                "default_val": 100000.0,
            }
            st.success(f"¡Rubro '{nuevo_nombre}' guardado con éxito!")
            st.rerun()

st.sidebar.markdown("---")
enable_preload = st.sidebar.checkbox(
    "Pre-cargar modelos (Click for Preload=True)",    
    value=False,
    help="Mantener modelos cargados en memoria de manera persistente.",
)

# ==========================================
# ENCABEZADO PRINCIPAL & DESCRIPCIÓN DEL RUBRO
# ==========================================
st.subheader(
    ":blue[LAYA - Motor de Decisiones Empresarial & Exposición Financiera]"
)
st.markdown(
    "Plataforma unificada con **Ingresa Multiformato**, **Persistencia SQLite**, **Rubros Dinámicos**, **Matriz de Riesgo Económico** y **Briefing Ejecutivo**."
)
st.markdown("---")
with st.container(border=True):
    current_config = RUBROS_CONFIG[selected_rubro_name]
    st.info(f"**Descripción del Rubro:** {current_config['description']}")

#st.markdown("---")

# ==========================================
# CARGA CACHEADA DEL MOTOR ROUTER LAYA
# ==========================================
@st.cache_resource
def load_laya_router(lang_choice, preload_flag):
    router = laya.Router(preload=preload_flag)
    if lang_choice == "English":
        router.load("english")
    else:
        router.load("multilingual")
    logging.info(
        f"Router LAYA cargado. Idioma: {lang_choice}, Preload: {preload_flag}"
    )
    return router


router = load_laya_router(lang_option, enable_preload)


# ==========================================
# EVALUACIÓN INDIVIDUAL CONCURRENTE
# ==========================================
def evaluar_registro(
    comment, router, current_config, base_val, lang_choice, threshold_val
):
    try:
        q_keys = list(current_config["questions"].keys())
        q_choice, q_score, q_noul = q_keys[0], q_keys[1], q_keys[2]

        predict_kwargs = {
            "state": comment,
            "questions": current_config["questions"],
        }
        if lang_choice != "automático":
            predict_kwargs["lang"] = lang_choice.lower()

        result = router.predict(**predict_kwargs)

        choice_answer = result["answers"][q_choice]["choice"]
        noul_answer = result["answers"][q_noul]["noul"]
        routing_model = result["routing"]["model"]

        score_data = result["answers"].get(q_score, {})
        score_val = score_data.get("score", 0)
        score_answer = score_data.get("legend", {}).get(
            str(round(score_val)), "neutral"
        )

        # Fallback por keywords si el modelo retorna 'other'
        if choice_answer == "other" and "keywords" in current_config:
            for cat, kws in current_config["keywords"].items():
                if any(kw in comment.lower() for kw in kws):
                    choice_answer = cat
                    logging.info(f"Fallback activado: 'other' mapeado a '{cat}'.")
                    break

        # Cálculo Exposición Financiera Esperada ($)
        financial_impact = noul_answer * base_val

        return {
            "comment": comment,
            "choice_answer": choice_answer,
            "noul_answer": noul_answer,
            "score_answer": score_answer,
            "score_val": score_val,
            "financial_impact": financial_impact,
            "routing_model": routing_model,
            "raw_result": result,
        }
    except Exception as e:
        logging.error(f"Error procesando registro: {str(e)}")
        return {"comment": comment, "error": str(e)}


# ==========================================
# INTERFAZ PRINCIPAL CON PESTAÑAS
# ==========================================
tab_eval, tab_history = st.tabs([
    "Evaluación & Exposición Financiera",
    "Histórico & Tendencias (SQLite)",
])

with tab_eval:
    st.subheader(":violet[1. Ingresa Multiformato de Datos]")

    input_method = st.radio(
        "Fuente de Datos:",
        ["Archivo (CSV / XLSX / TXT)", "Ingreso Manual (Texto)"],
        horizontal=True,
    )
    comments_list = []

    if input_method == "Archivo (CSV / XLSX / TXT)":
        uploaded_file = st.file_uploader(
            "Cargar archivo", type=["csv", "xlsx", "txt"]
        )
        if uploaded_file:
            if uploaded_file.name.endswith(".csv"):
                df_up = pd.read_csv(uploaded_file)
                col_selected = st.selectbox(
                    "Selecciona la columna con los comentarios:", df_up.columns
                )
                comments_list = df_up[col_selected].dropna().astype(str).tolist()
            elif uploaded_file.name.endswith(".xlsx"):
                df_up = pd.read_excel(uploaded_file)
                col_selected = st.selectbox(
                    "Selecciona la columna con los comentarios:", df_up.columns
                )
                comments_list = df_up[col_selected].dropna().astype(str).tolist()
            elif uploaded_file.name.endswith(".txt"):
                lines = uploaded_file.read().decode("utf-8").split("\n")
                comments_list = [l.strip() for l in lines if l.strip()]

            st.success(f"Cargados {len(comments_list)} registros correctamente.")
    else:
        raw_txt = st.text_area(
            "Ingresa un comentario por línea:",
            height=150,
            placeholder=current_config["placeholder"],
        )
        if raw_txt.strip():
            comments_list = [l.strip() for l in raw_txt.split("\n") if l.strip()]

    btn_eval = st.button("Ejecutar Evaluación de Decisiones", type="primary")

    if btn_eval and comments_list:
        st.info(
            f"Procesando {len(comments_list)} registros de forma concurrente con el"
            f" motor LAYA ({lang_option})..."
        )
        results = []
        progress_bar = st.progress(0)

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                executor.submit(
                    evaluar_registro,
                    c,
                    router,
                    current_config,
                    unit_financial_value,
                    lang_option,
                    threshold_value,
                ): c
                for c in comments_list
            }
            completed = 0
            for f in concurrent.futures.as_completed(futures):
                res = f.result()
                results.append(res)
                completed += 1
                progress_bar.progress(completed / len(comments_list))

        progress_bar.empty()
        df_res = pd.DataFrame([r for r in results if "error" not in r])

        if not df_res.empty:
            # Guardar automáticamente en SQLite
            guardar_evaluaciones_db(df_res, selected_rubro_name)

            # ==========================================
            #  RESUMEN EJECUTIVO DE EVALUACIÓN
            # ==========================================
            st.markdown("---")
            st.markdown("### :material/rate_review: Resumen Ejecutivo de Evaluación")

            with st.container(border=True):
                label_col1, label_col2, label_col3 = current_config["metric_labels"]

                df_choice = (
                    df_res["choice_answer"].str.title().value_counts().reset_index()
                )
                df_choice.columns = [label_col1, "Cantidad"]

                df_score = (
                    df_res["score_answer"].str.title().value_counts().reset_index()
                )
                df_score.columns = [label_col2, "Cantidad"]

                noul_counts = (df_res["noul_answer"] >= threshold_value).value_counts()
                df_noul = pd.DataFrame([
                    {
                        label_col3: "SÍ (Alta Probabilidad)",
                        "Cantidad": noul_counts.get(True, 0),
                    },
                    {
                        label_col3: "NO (Baja Probabilidad)",
                        "Cantidad": noul_counts.get(False, 0),
                    },
                ])

                col_sum1, col_sum2, col_sum3 = st.columns(3)
                with col_sum1:
                    st.markdown(f"**{label_col1}:**")
                    st.dataframe(df_choice, hide_index=True, width="stretch")
                with col_sum2:
                    st.markdown(f"**{label_col2}:**")
                    st.dataframe(df_score, hide_index=True, width="stretch")
                with col_sum3:
                    st.markdown(f"**{label_col3}:**")
                    st.dataframe(df_noul, hide_index=True, width="stretch")

                st.markdown("---")

                col_info_sum, col_btn_csv, col_btn_excel = st.columns([2, 1, 1])
                with col_info_sum:
                    st.markdown(
                        f"**Total registros procesados:** {len(df_res)} | **Rubro:**"
                        f" {selected_rubro_name}"
                    )
                with col_btn_csv:
                    csv_data = (
                        df_res[[
                            "comment",
                            "choice_answer",
                            "score_answer",
                            "noul_answer",
                            "routing_model",
                            "financial_impact",
                        ]]
                        .to_csv(index=False)
                        .encode("utf-8")
                    )
                    st.download_button(
                        label=":material/download: Descargar CSV",
                        data=csv_data,
                        file_name=(
                            "laya_evaluacion_"
                            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                        ),
                        mime="text/csv",
                        width="stretch",
                    )
                with col_btn_excel:
                    df_export = df_res[[
                        "comment",
                        "choice_answer",
                        "score_answer",
                        "noul_answer",
                        "routing_model",
                        "financial_impact",
                    ]].rename(columns={
                        "comment": "Comentario",
                        "choice_answer": label_col1,
                        "score_answer": label_col2,
                        "noul_answer": f"Prob. {label_col3}",
                        "routing_model": "Modelo LAYA",
                        "financial_impact": "Exposición Esperada ($)"
                    })
                    excel_data = to_excel(df_export)
                    st.download_button(
                        label=":material/download: Descargar Excel",
                        data=excel_data,
                        file_name=(
                            "laya_evaluacion_"
                            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                        ),
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        width="stretch",
                    )

            # ==========================================
            # MÉTRICAS FINANCIERAS Y DE RIESGO
            # ==========================================
            st.markdown("---")
            st.markdown("### Matriz de Exposición Financiera y Riesgo")

            total_eval = len(df_res)
            high_risk_df = df_res[df_res["noul_answer"] >= threshold_value]
            total_high_risk = len(high_risk_df)
            total_financial_exposure = df_res["financial_impact"].sum()
            critical_financial_exposure = high_risk_df["financial_impact"].sum()

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Registros Evaluados", total_eval)
            m2.metric(
                "Casos de Alerta Crítica",
                total_high_risk,
                delta=f"{(total_high_risk/total_eval):.1%}",
            )
            m3.metric(
                "Pérdida/Riesgo Total Esperado", f"${total_financial_exposure:,.2f}"
            )
            m4.metric(
                "Riesgo Financiero Crítico",
                f"${critical_financial_exposure:,.2f}",
                delta="Atención Prioritaria",
            )

            st.markdown("---")

            # SÍNTESIS EJECUTIVA AUTOMATIZADA
            top_cat = df_res["choice_answer"].value_counts().index[0]
            top_cat_pct = (
                df_res["choice_answer"].value_counts().iloc[0] / total_eval
            ) * 100

            st.markdown("### Briefing Ejecutivo Automatizado")
            st.info(
                f"**Diagnóstico Operativo:** Durante esta corrida en el rubro"
                f" **{selected_rubro_name}**, se identificó que la categoría"
                f" dominante es **'{top_cat.upper()}'** con un"
                f" **{top_cat_pct:.1f}%** de los mensajes.\n\n**Análisis de"
                " Exposición Financiera:** Se registraron **{total_high_risk} casos"
                f" sobre el umbral de criticidad ({threshold_value:.0%})**,"
                " representando una **exposición económica inmediata de"
                f" ${critical_financial_exposure:,.2f}**. Se recomienda focalizar el"
                " equipo de operaciones en la resolución de los casos críticos para"
                f" mitigar el {label_col3}."
            )

            # GRÁFICOS INTERACTIVOS
            st.markdown("#### Distribución y Severidad")
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                st.markdown(f"**Volumen por {label_col1}**")
                st.bar_chart(df_res["choice_answer"].value_counts())
            with col_g2:
                st.markdown("**Exposición Financiera ($) por Categoría**")
                st.bar_chart(df_res.groupby("choice_answer")["financial_impact"].sum())

            # TABLA DE DETALLE PONDERADA POR RIESGO
            st.markdown("#### Detalle de Registros (Ordenado por Exposición Financiera)")
            df_show = df_res.sort_values(by="financial_impact", ascending=False)
            st.dataframe(
                df_show[[
                    "comment",
                    "choice_answer",
                    "score_answer",
                    "noul_answer",
                    "financial_impact",
                ]].rename(
                    columns={
                        "comment": "Comentario",
                        "choice_answer": label_col1,
                        "score_answer": label_col2,
                        "noul_answer": f"Prob. {label_col3}",
                        "financial_impact": "Exposición Esperada ($)",
                    }
                ),
                width="stretch",
            )

            # DETALLE TÉCNICO EN JSON
            with st.expander(":material/manage_search: Inspeccionar Respuestas JSON Crudas (Auditoría LAYA)"):
                for item in results:
                    if "raw_result" in item:
                        st.write(f"**Texto:** {item['comment']}")
                        st.code(
                            json.dumps(item["raw_result"], indent=2, ensure_ascii=False),
                            language="json",
                        )

# ==========================================
# PESTAÑA HISTÓRICO Y TENDENCIAS (SQLite)
# ==========================================
with tab_history:
    st.subheader("Histórico de Decisiones y Tendencias Temporal")
    conn = sqlite3.connect(DB_FILE)
    df_db = pd.read_sql_query(
        "SELECT * FROM evaluacion_historica ORDER BY id DESC", conn
    )
    conn.close()

    if df_db.empty:
        st.warning("Aún no hay evaluaciones registradas en el histórico.")
    else:
        st.markdown(f"**Total de evaluaciones almacenadas:** {len(df_db)}")

        rubro_filter = st.selectbox(
            "Filtrar Histórico por Rubro:",
            ["Todos"] + list(BASE_RUBROS_CONFIG.keys()),
        )
        if rubro_filter != "Todos":
            df_filtered = df_db[df_db["rubro"] == rubro_filter]
        else:
            df_filtered = df_db

        h1, h2 = st.columns(2)
        with h1:
            st.metric(
                "Total Acumulado Exposición Financiera",
                f"${df_filtered['impacto_financiero'].sum():,.2f}",
            )
        with h2:
            st.metric(
                "Promedio Probabilidad de Riesgo",
                f"{df_filtered['prob_riesgo'].mean():.2%}",
            )

        col_h_txt, col_h_excel = st.columns([3, 1])
        with col_h_txt:
            st.markdown("#### Evolución de Evaluación por Rubro")
        with col_h_excel:
            hist_excel = to_excel(df_filtered)
            st.download_button(
                label=":material/download: Descargar Histórico Excel",
                data=hist_excel,
                file_name=f"laya_historico_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                width="stretch",
            )
            
        st.dataframe(df_filtered, width="stretch")