import streamlit as st
import pandas as pd
from datetime import datetime

# --- SIVUN ASETUKSET ---
st.set_page_config(
    page_title="Tonttiseuranta Oulu",
    page_icon="🏙️",
    layout="wide"
)

# --- TYYLIT ---
st.markdown("""
<style>
    body {
        background-color: #f0f4f9;
    }
    .decision-card {
        background: linear-gradient(135deg, #e8f1ff 0%, #ffffff 100%);
        color: #003366;
        padding: 1.2rem;
        margin-bottom: 1rem;
        border-radius: 12px;
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease-in-out;
        border-left: 6px solid #0066cc;
    }
    .decision-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 14px rgba(0, 0, 0, 0.15);
    }
    a {
        text-decoration: none;
        color: #0047b3;
        font-weight: 600;
    }
    a:hover {
        color: #003080;
        text-decoration: underline;
    }
    .decision-title {
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

# --- OTSIKKO ---
st.title("🏙️ Oulun viranhaltijapäätökset – Tonttiseuranta")
st.caption(f"Päivitetty: {datetime.now().strftime('%d.%m.%Y %H:%M')}")

st.markdown("""
Tämä sovellus hakee ja näyttää Oulun kaupungin viranhaltijoiden **tontteihin liittyviä päätöksiä**  
(esimerkiksi vuokraukset, myynnit ja varaukset).
""")

st.divider()

# --- LADATAAN CSV ---
try:
    df = pd.read_csv("data/oulu_viranhaltijapaatokset.csv")

    # --- HAKU ---
    haku = st.text_input("🔍 Hae päätöksiä otsikon perusteella:")
    if haku:
        df = df[df["otsikko"].str.contains(haku, case=False, na=False)]

    st.markdown(f"**Näytetään {len(df)} päätöstä**")

    # --- KORTTINÄKYMÄ ---
    for _, row in df.iterrows():
        st.markdown(f"""
        <div class="decision-card">
            <div class="decision-title">{row['otsikko']}</div>
            <p>🔗 <a href="{row['linkki']}" target="_blank">Avaa päätös Oulun sivuilla</a></p>
        </div>
        """, unsafe_allow_html=True)

except FileNotFoundError:
    st.error("CSV-tiedostoa ei löytynyt! Aja ensin `tonttiseuranta.py` tiedoston luomiseksi.")
