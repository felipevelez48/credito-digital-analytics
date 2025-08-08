# Crédito-digital-analytics

Repositorio reproducible (VS Code + Python) que integra: (1) limpieza y tipado de la base (Excel → Parquet), (2) EDA con hallazgos accionables, (3) un modelo base de desistimiento (pipeline scikit‑learn + umbral óptimo) y (4) un dashboard en Streamlit con filtros, KPIs y scoring descargable. Con este flujo mostramos cómo pasar de datos crudos a insights y a una herramienta utilizable por negocio en pocas horas, sin servicios pagos.

---

## 🚀 Objetivos

- Parte I (diseño de medición): Proponer y documentar el experimento para evaluar el cambio de envío de estados de cuenta de físico → e‑mail sin afectar la recuperación de cartera.

- Parte II (análisis y modelo):

    - Identificar el cliente objetivo (socio‑demo y comportamiento crédito).

    - Detectar diferencias por periodos del año.

    - Perfilar a los aprobados.

    - Entrenar un modelo para predecir desistimiento.

    ---

## 🗂️ Estructura del repositorio
```
.
├── app/                    # Streamlit app
│   └── app.py
├── data/
│   ├── raw/                # Excel original
│   └── processed/          # Parquet limpio
├── docs/
│   └── experimento_ab_test.md
├── models/                 # model_desist.pkl + meta
├── notebooks/
│   ├── 00_ingesta_limpieza.ipynb
│   ├── 01_eda.ipynb
│   └── 02_features_modelo.ipynb
├── reports/
│   ├── figures/            # Imágenes exportadas
├── requirements.txt
└── README.md
```

---

## 🧰 Instalación y ejecución (Windows / Git Bash)

```
# 1) Clonar
git clone https://github.com/felipevelez48/credito-digital-analytics.git
cd credito-digital-analytics

# 2) Entorno virtual
python -m venv venv
source venv/Scripts/activate

# 3) Dependencias
pip install -r requirements.txt

# 4) Datos
# Copiar el archivo "Base PRUEBA - ANALITICA.xlsx" a data/raw/

# 5) Jupyter (opcional para notebooks)
jupyter lab  # o code notebooks/*.ipynb desde VS Code (kernel del venv)

# 6) Dashboard Streamlit
streamlit run app/app.py
```

-**Nota:** Si VS Code no muestra el kernel del venv, seleccionar Python: Select Interpreter y apuntar a venv/Scripts/python.exe.

## 🔍 EDA – Hallazgos (resumen)

Ver notebooks/01_eda.ipynb y carpeta reports/figures para detalles y gráficos.

**- Edad:** concentración en rangos 20–34 años (ej. distribución por edad_grupo).

**- Estacionalidad:** variación por trimestre en volumen de solicitudes y composición de estados (gráfico por periodo).

**- Aprobados vs. otros:** diferencias en ingresos, endeudamiento y otras variables financieras.

(Los valores exactos quedan en el EDA; este README resume.)

---

## 🤖 Modelo de desistimiento (Parte II‑4)
**Variable objetivo:** estado → binario (DESISTIDA=1, resto=0)

**Pipeline**

- Preprocesamiento con ColumnTransformer:

    - Numéricas → StandardScaler

    - Categóricas → OneHotEncoder(handle_unknown='ignore')

- Modelos evaluados (CV=5, ROC‑AUC):

    - Logistic Regression (class_weight='balanced') → ~0.626 ± 0.006

    - Random Forest (n_estimators=300) → ~0.613 ± 0.047

- Tuning ligero (GridSearch con saga): mejor combinación L1, C=0.1 ≈ 0.627 ROC‑AUC.

**Restricción práctica:** equipo local con poco poder de cómputo. El tuning extenso (muchas combinaciones / modelos más pesados) incrementa significativamente el tiempo y uso de memoria. Se priorizó un baseline estable e interpretable.

**Métricas en holdout**

- notebooks/02_features_modelo.ipynb calcula:

    - ROC‑AUC en test

    - Confusion matrix y classification report (accuracy, precision, recall, f1)

    - Umbral óptimo (max F1 de clase positiva)

- Artefactos guardados en models/:

    - model_desist.pkl (pipeline completo)

    - model_meta.json (ROC‑AUC, umbral)

**Criterios de selección**

- 1. ROC‑AUC como métrica primaria por balance‑desbalance de clases.

- 2. Interpretabilidad y costo computacional (LogReg sobre RandomForest por estabilidad / CPU / RAM en este caso).

- 3. Tiempo de inferencia bajo y facilidad de despliegue.

## 📊 Dashboard (Streamlit)

- **Filtros:** año, zona, género, etc.

- **KPIs:** registros filtrados, prob. media de desistir, conteo de marcados según umbral.

- **Tabla:** top solicitudes por probabilidad de desistir + descarga CSV.

- **Umbral ajustable** desde la barra lateral, usando el valor óptimo calculado.

**Ejecutar**
```
streamlit run app/app.py
```
Opciones de despliegue gratis:

- Streamlit Community Cloud (demo pública rápida)

- Servidor propio / contenedor Docker en infraestructura interna.

---

## 🧪 Parte I – Diseño de medición (físico vs. e‑mail)

**Hipótesis del jefe de cartera:** Enviar por e‑mail bajará la recuperación de cartera.

**Diseño propuesto (A/B):** ver documento: docs/experimento_ab_test.md.

- Asignación aleatoria 50/50 (físico vs. e‑mail), estratificada por segmento (edad, zona, riesgo).

- Métrica primaria: tasa de pago puntual a 30 días; secundarias: días de mora, % pagos totales.

- Horizonte mínimo: calcular tamaño de muestra para detectar Δ=2 pp con poder 0.8 y α=0.05.

- Seguimiento: corte semanal, análisis por intención de tratar (ITT), chequeo de balance.

---

## 🧠 Aprendizajes clave

**- Modelado local ≠ ilimitado:** con 8 GB RAM, el tuning masivo no escala; mejor baseline limpio + mejoras incrementales.

**- Logística ≈ buen primer modelo:** interpretable, rápido y con performance decente.

**- Streamlit** es fundamental para socializar resultados y probar escenarios (what‑if); su adopción interna es simple.

**- Exportables claros** (figuras, parquet, pkl) aceleran la presentación y el traspaso a equipos de ingeniería.

---

## 🔭 Roadmap / Próximos pasos

- 1. Feature engineering adicional (ej.: ratios de esfuerzo, log1p en colas, binning de variables continuas).

- 2. Modelos: HistGradientBoostingClassifier, XGBoost (CPU), calibración de probabilidades (Platt/Isotonic).

- 3. MLOps ligero:

    - Fijar versiones (con pip-tools o requirements.lock).

    - GitHub Actions (lint/test) en cada push.

    - script de inferencia por lotes (CLI) y endpoint simple (FastAPI opcional).

- 4. Despliegue:

    - Demo en Streamlit Cloud.

    - Docker + despliegue interno (on‑prem o VM).

- 5. Parte I (operativa): instrumentar el A/B en la operación real con tableros de seguimiento.

---

## 📚 Referencias rápidas

- Scikit‑learn: Pipelines, ColumnTransformer, LogisticRegression, RandomForest.

- Plotly + Kaleido: exportación de imágenes.

- Streamlit: desplegar dashboards rápidamente.

---

# 💡 Autor 📊🤖
## John Felipe Vélez
### Data Engineer