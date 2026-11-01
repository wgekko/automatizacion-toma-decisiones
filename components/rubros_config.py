# rubros_config.py

BASE_RUBROS_CONFIG = {
    "E-commerce / Retail (Atención al Cliente)": {
        "description": "Clasificación de comentarios, detección de departamentos y riesgo de churn.",
        "placeholder": "Ejemplo:\nEl producto llegó roto y tardaron semanas. Exijo reintegro o cancelo la suscripción.",
        "questions": {
            "department": {
                "type": "choice", 
                "instructions": "Qué departamento debería manejar este caso?",
                "criteria": {
                    "facturacion": "facturas, pagos, reembolsos, cobros",
                    "tecnologia": "bugs, caídas de sistema, problemas técnicos",
                    "logistica": "entregas, envíos, devoluciones, tracking",
                    "ventas": "consultas de ventas, precios, promociones",
                    "servicio al cliente": "atención, soporte, ayuda, quejas",
                    "other": "everything else"
                }
            },
            "sentiment": {
                "type": "score", 
                "instructions": "Cuál es el sentimiento del cliente?",
                "criteria": ["negativo", "neutral", "positivo"]
            },
            "churn_risk": {
                "type": "noul", 
                "instructions": "¿El usuario amenaza con cancelar o abandonar el servicio?"
            }
        },
        "keywords": {
            "facturacion": ["factura", "pago", "reembolso", "cobro"],
            "tecnologia": ["bug", "error", "sistema", "fallo"],
            "ventas": ["venta", "precio", "promoción"],
            "logistica": ["entrega", "envío", "devolución"],
            "servicio al cliente": ["soporte", "ayuda", "queja"]
        },
        "metric_labels": ("Departamento", "Sentimiento", "Riesgo Churn"),
        "financial_label": "Valor Promedio del Cliente (CLV) ($)",
        "default_val": 120000.0
    },
    "Servicios Financieros & Fintech (Banca & Cobranzas)": {
        "description": "Análisis de consultas financieras, solicitudes de créditos, tarjetas y fraudes.",
        "placeholder": "Ejemplo:\nDesconozco el último cobro de $50000 en mi tarjeta de crédito. Iré al Banco Central.",
        "questions": {
            "fin_category": {
                "type": "choice", 
                "instructions": "A qué área financiera corresponde la consulta?",
                "criteria": {
                    "tarjetas": "tarjetas de crédito, débito, reposición",
                    "prestamos": "créditos, préstamos personales, financiación",
                    "fraude": "desconocimiento de compra, robo, estafa",
                    "inversiones": "plazo fijo, fondos comunes, dólares",
                    "other": "everything else"
                }
            },
            "risk_sentiment": {
                "type": "score", 
                "instructions": "Cuál es el nivel de estrés o criticidad del cliente?",
                "criteria": ["tranquilo", "preocupado", "alarmado / furioso"]
            },
            "legal_threat": {
                "type": "noul", 
                "instructions": "¿El usuario menciona acciones legales o defensa al consumidor?"
            }
        },
        "keywords": {
            "tarjetas": ["tarjeta", "débito", "crédito"],
            "prestamos": ["préstamo", "crédito", "cuotas"],
            "fraude": ["desconocimiento", "robo", "estafa", "no hice"],
            "inversiones": ["plazo fijo", "dólares", "invertir"]
        },
        "metric_labels": ("Área Financiera", "Criticidad", "Amenaza Legal"),
        "financial_label": "Contingencia Promedio por Reclamo Legal/Fraude ($)",
        "default_val": 250000.0
    },
    "Salud & Clínicas (Gestión de Turnos y Pacientes)": {
        "description": "Triaje automatizado de mensajes de pacientes, turnos y urgencias médicas.",
        "placeholder": "Ejemplo:\nTengo dolor agudo en el pecho y no hay turnos disponible. Negligencia total.",
        "questions": {
            "medical_category": {
                "type": "choice", 
                "instructions": "A qué servicio médico está orientada la solicitud?",
                "criteria": {
                    "turnos": "asignación, reprogramación, cita médica",
                    "recetas": "receta electrónica, medicación crónica",
                    "urgencias": "dolor agudo, fiebre, guardia, emergencia",
                    "facturacion_os": "obra social, prepaga, bonos, coseguros",
                    "other": "everything else"
                }
            },
            "urgency_score": {
                "type": "score", 
                "instructions": "Cuál es el nivel de urgencia clínica percibida?",
                "criteria": ["baja", "moderada", "alta / emergente"]
            },
            "severe_complaint": {
                "type": "noul", 
                "instructions": "¿El paciente manifiesta una queja grave por mala praxis o demora extrema?"
            }
        },
        "keywords": {
            "turnos": ["turno", "cita", "reprogramar"],
            "recetas": ["receta", "medicamento"],
            "urgencias": ["urgencia", "emergencia", "dolor", "guardia"],
            "facturacion_os": ["obra social", "prepaga", "coseguro"]
        },
        "metric_labels": ("Servicio Médico", "Nivel Urgencia", "Queja Severa"),
        "financial_label": "Costo de Riesgo Operativo / Mala Praxis ($)",
        "default_val": 500000.0
    },
    "Inmobiliaria & Real Estate (Gestión de Leads)": {
        "description": "Clasificación de consultas sobre propiedades, intención de compra/alquiler y urgencia.",
        "placeholder": "Ejemplo:\nQuiero comprar el departamento en Godoy Cruz, tengo la seña lista para coordinar hoy.",
        "questions": {
            "operation_type": {
                "type": "choice", 
                "instructions": "Qué tipo de operación inmobiliaria busca el cliente?",
                "criteria": {
                    "compra": "comprar casa, departamento, terreno",
                    "alquiler": "alquilar vivienda, contrato",
                    "tasacion": "tasar propiedad, vender mi casa",
                    "mantenimiento": "reparaciones, expensas",
                    "other": "everything else"
                }
            },
            "interest_level": {
                "type": "score", 
                "instructions": "Cuál es el nivel de interés y seriedad del lead?",
                "criteria": ["bajo", "moderado", "alto"]
            },
            "immediate_action": {
                "type": "noul", 
                "instructions": "¿El cliente solicita una visita o seña inmediata?"
            }
        },
        "keywords": {
            "compra": ["comprar", "venta", "terreno"],
            "alquiler": ["alquilar", "alquiler"],
            "tasacion": ["tasar", "vender"],
            "mantenimiento": ["expensas", "rotura"]
        },
        "metric_labels": ("Operación", "Interés Lead", "Acción Inmediata"),
        "financial_label": "Comisión Inmobiliaria Estimada ($)",
        "default_val": 800000.0
    },
    "Recursos Humanos / RRHH (Gestión de Talentos)": {
        "description": "Filtrado automático de postulaciones, clima laboral y riesgo de renuncia.",
        "placeholder": "Ejemplo:\nLas condiciones actuales son insostenibles, estoy evaluando ofertas en otra empresa.",
        "questions": {
            "hr_category": {
                "type": "choice", 
                "instructions": "Qué tópico de Recursos Humanos aborda el mensaje?",
                "criteria": {
                    "reclutamiento": "cv, postulación, entrevista",
                    "nomina_beneficios": "sueldo, recibo de haberes, vacaciones",
                    "clima_laboral": "ambiente, conflicto, condiciones",
                    "capacitacion": "cursos, talleres",
                    "other": "everything else"
                }
            },
            "employee_sentiment": {
                "type": "score", 
                "instructions": "Cuál es el estado anímico o satisfacción del empleado?",
                "criteria": ["motivado", "neutral", "desmotivado / frustrado"]
            },
            "attrition_risk": {
                "type": "noul", 
                "instructions": "¿El colaborador expresa intención clara de renunciar?"
            }
        },
        "keywords": {
            "reclutamiento": ["cv", "postulación", "puesto"],
            "nomina_beneficios": ["sueldo", "vacaciones"],
            "clima_laboral": ["clima", "jefe", "estrés"],
            "capacitacion": ["curso", "capacitación"]
        },
        "metric_labels": ("Tópico RRHH", "Estado Anímico", "Riesgo Renuncia"),
        "financial_label": "Costo de Rotación / Reemplazo de Puesto ($)",
        "default_val": 1500000.0
    },
    "Logística y Cadena de Suministro (Envíos & Tracking)": {
        "description": "Monitoreo de entregas, reclamos por paquetes demorados, dañados o extraviados.",
        "placeholder": "Ejemplo:\nEl paquete figura como entregado pero nunca llegó a mi domicilio. Exijo devolución del dinero.",
        "questions": {
            "logistics_category": {
                "type": "choice", 
                "instructions": "Cuál es la incidencia logística reportada?",
                "criteria": {
                    "retraso": "paquete demorado, fecha vencida, tracking sin actualizar",
                    "producto_danado": "roto, dañado, en mal estado, faltante",
                    "direccion_erronea": "dirección incorrecta, no encuentra el domicilio",
                    "devolucion": "retorno, cambio de producto, reenvío",
                    "other": "everything else"
                }
            },
            "customer_mood": {
                "type": "score", 
                "instructions": "Cuál es el sentimiento del clienteafectado?",
                "criteria": ["calmo", "molesto", "indignado"]
            },
            "legal_demand_risk": {
                "type": "noul", 
                "instructions": "¿El cliente exige compensación económica o demanda formal?"
            }
        },
        "keywords": {
            "retraso": ["demora", "retrasado", "tarde", "no llega"],
            "producto_danado": ["roto", "dañado", "golpeado", "faltante"],
            "direccion_erronea": ["dirección", "ubicación", "perdió"],
            "devolucion": ["devolución", "cambio", "retorno"]
        },
        "metric_labels": ("Incidencia", "Sentimiento", "Riesgo Demanda"),
        "financial_label": "Costo por Incidencia / Compensación Logística ($)",
        "default_val": 180000.0
    }
}