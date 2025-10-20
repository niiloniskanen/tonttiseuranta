import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import pdfplumber
from urllib.parse import urljoin
import os

# --- ASETUKSET ---
BASE_URL = "https://asiakirjat.ouka.fi"
LISTING_URL = "https://asiakirjat.ouka.fi/ktwebscr/vparlist_tweb.htm"
HAKUSANAT = ["tontti", "vuokra", "varaaminen", "myynti", "myyminen", "maa-alue", "kiinteistö", "luovutus"]

# --- PDF:N LUKU ---
def hae_pdf_teksti(url):
    """Lataa ja lukee PDF:n tekstin, palauttaa sen merkkijonona"""
    try:
        r = requests.get(url)
        r.raise_for_status()
        # väliaikainen PDF
        pdf_path = "temp.pdf"
        with open(pdf_path, "wb") as f:
            f.write(r.content)
        teksti = ""
        with pdfplumber.open(pdf_path) as pdf:
            for sivu in pdf.pages:
                teksti += sivu.extract_text() or ""
        os.remove(pdf_path)
        return teksti
    except Exception as e:
        print(f"⚠️ PDF:n lukeminen epäonnistui {url}: {e}")
        return ""

# --- HAE SIVU ---
resp = requests.get(LISTING_URL)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, "html.parser")

# --- POIMI LINKIT JA OTSIKOT ---
paatokset = []
for a in soup.find_all("a", href=True):
    otsikko = a.get_text(strip=True)
    href = a["href"]
    full_link = urljoin(BASE_URL, href)

    # Tarkistetaan otsikosta
    osuma_otsikossa = any(re.search(sana, otsikko, re.IGNORECASE) for sana in HAKUSANAT)

    # Jos linkki on PDF, tarkista myös sisällöstä
    osuma_pdfssa = False
    if href.lower().endswith(".pdf"):
        pdf_teksti = hae_pdf_teksti(full_link)
        osuma_pdfssa = any(re.search(sana, pdf_teksti, re.IGNORECASE) for sana in HAKUSANAT)

    if osuma_otsikossa or osuma_pdfssa:
        paatokset.append({
            "otsikko": otsikko,
            "linkki": full_link
        })

# --- TALLENNA TULOKSET ---
os.makedirs("data", exist_ok=True)  # varmistetaan että data-kansio on olemassa
if paatokset:
    df = pd.DataFrame(paatokset)
    df.to_csv("data/oulu_viranhaltijapaatokset.csv", index=False, encoding="utf-8-sig")
    print(f"Tallennettu {len(df)} päätöstä CSV-tiedostoon.")
else:
    print("Ei löytynyt hakusanoihin vastaavia päätöksiä listauksesta.")
