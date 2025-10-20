import streamlit as st
import pandas as pd

# Sivun asetukset
st.set_page_config(page_title="Tonttiseuranta", layout="wide")

st.title("Oulun viranhaltijapäätökset – tonttiseuranta")

st.markdown(
    """
    Tämä Streamlit-sovellus näyttää Oulun kaupungin viranhaltijapäätökset, 
    jotka on haettu verkkosivuilta ja tallennettu CSV-tiedostoon.  
    Klikkaa linkkejä avataksesi alkuperäiset päätökset
    """
)

try:
    # Lue CSV-tiedosto
    df = pd.read_csv("data/oulu_viranhaltijapaatokset.csv")

    # Jos linkkikolumni on olemassa, muutetaan se HTML-linkiksi
    if "linkki" in df.columns:
        df["linkki"] = df["linkki"].apply(
            lambda x: f'<a href="{x}" target="_blank">🔗 Avaa päätös</a>'
            if pd.notna(x) else ""
        )

    # Näytetään taulukko HTML:nä (tämä sallii linkit)
    st.markdown("### Päätökset")
    st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)

except FileNotFoundError:
    st.warning("CSV-tiedostoa ei löytynyt! Aja ensin `tonttiseuranta.py` datan hakemiseksi.")
except Exception as e:
    st.error(f"Tapahtui virhe: {e}")
