import streamlit as st
import pandas as pd
import joblib, json
from pathlib import Path

st.set_page_config(page_title="Crédito Digital – Perfil & Desistimiento", layout="wide")

@st.cache_resource
def load_model():
    model = joblib.load("models/model_desist.pkl")
    meta  = json.load(open("models/model_meta.json"))
    return model, meta

@st.cache_data
def load_data():
    return pd.read_parquet("data/processed/creditos.parquet")

df = load_data()
model, meta = load_model()
thr = st.sidebar.slider("Umbral (prob. desistir)", min_value=0.05, max_value=0.95, value=float(meta["threshold"]), step=0.01)

# ---- Filtros básicos
st.sidebar.subheader("Filtros")
anio = st.sidebar.multiselect("Año", sorted(df["anio"].dropna().unique().tolist()))
zona = st.sidebar.multiselect("Zona", sorted(df["zona"].dropna().unique().tolist()))
genero = st.sidebar.multiselect("Género", sorted(df["genero"].dropna().unique().tolist()))

mask = pd.Series(True, index=df.index)
if anio:   mask &= df["anio"].isin(anio)
if zona:   mask &= df["zona"].isin(zona)
if genero: mask &= df["genero"].isin(genero)

sub = df.loc[mask].copy()

# ---- Scoring
X_sub = sub.drop(columns=["estado"])
proba = model.predict_proba(X_sub)[:, 1]
sub["prob_desistir"] = proba
sub["flag_desistir"] = (sub["prob_desistir"] >= thr).astype(int)

# ---- KPIs
c1, c2, c3 = st.columns(3)
c1.metric("Registros filtrados", f"{len(sub):,}")
c2.metric("Prob. media desistir", f"{sub['prob_desistir'].mean():.2%}")
c3.metric("Marcados como 'desistir'", int(sub["flag_desistir"].sum()))

# ---- Vista y descarga
st.markdown("### Top clientes con mayor probabilidad de desistir")
st.dataframe(sub.sort_values("prob_desistir", ascending=False)
               .head(100)[["solicitud","prob_desistir","estado","ingresos","edad","zona","genero"]]
               .style.format({"prob_desistir": "{:.2%}"}))

st.download_button(
    "Descargar CSV filtrado + scoring",
    sub.to_csv(index=False).encode("utf-8"),
    "scoring_desistimiento.csv",
    "text/csv"
)
