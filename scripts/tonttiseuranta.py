import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from urllib.parse import urljoin

# --- ASETUKSET ---
BASE_URL = "https://www.ouka.fi"
LISTING_URL = "https://asiakirjat.ouka.fi/ktwebscr/vparlist_tweb.htm"  # voit myöhemmin säätää tarkemmaksi
HAKUSANAT = ["tontti", "vuokra", "varaaminen", "myynti", "myyminen", "maa-alue", "kiinteistö", "luovutus"]

# --- HAE SIVU ---
resp = requests.get(LISTING_URL)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, "html.parser")

# --- POIMI LINKIT JA OTSIKOT ---
paatokset = []
for a in soup.find_all("a", href=True):
    otsikko = a.get_text(strip=True)
    href = a["href"]
    # filtteröi hakusanoilla
    if any(re.search(sana, otsikko, re.IGNORECASE) for sana in HAKUSANAT):
        full_link = urljoin(BASE_URL, href)
        paatokset.append({
            "otsikko": otsikko,
            "linkki": full_link
        })

# --- TALLENNA TULOKSET ---
if paatokset:
    df = pd.DataFrame(paatokset)
    df.to_csv("oulu_viranhaltijapaatokset.csv", index=False, encoding="utf-8-sig")
    print(f"Tallennettu {len(df)} päätöstä CSV-tiedostoon.")
else:
    print("Ei löytynyt vastaavia päätöksiä listauksesta.")
