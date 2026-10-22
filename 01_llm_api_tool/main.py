"""Domáca úloha 1: LLM, ktorý si zavolá nástroj.

Čo skript robí, v štyroch krokoch:
  1. Pošle Gemini otázku a povie mu, že existuje nástroj px_na_mm.
  2. Gemini odpovie pokynom "zavolaj px_na_mm s týmito číslami".
  3. My funkciu u seba spustíme a dostaneme výsledok.
  4. Výsledok pošleme Gemini späť a on z neho napíše finálnu odpoveď.

Návod, ako to spustiť, a vysvetlenie rozhodnutí je v README.md.
"""

import os  # os = prístup k systému; použijeme ho na prečítanie API kľúča

from dotenv import load_dotenv  # načíta súbor .env (tam je náš tajný kľúč)
from google import genai  # oficiálna knižka od Googlu na rozprávanie s Gemini
from google.genai import types  # pomocné "tvary" správ, napr. popis nástroja

# Model, ktorý použijeme. "flash" = rýchly a lacný model, na túto úlohu úplne stačí.
# Lektor v príklade používa "gemini-2.5-flash", ale ten už Google pre nových
# používateľov vypol (chyba 404). Najnovší "gemini-3.8-flash" je zase práve
# preťažený (chyba 503), preto berieme o stupeň starší, ktorý odpovedá spoľahlivo.
MODEL = "gemini-3.7-flash"


# ---------------------------------------------------------------------------
# NÁSTROJ: funkcia, ktorú bude môcť LLM "zavolať".
# ---------------------------------------------------------------------------
def px_na_mm(pixely: float, dpi: float) -> float:
    """Prepočíta pixely na milimetre pre dané rozlíšenie (dpi).

    Prečo je to dobrý nástroj: LLM je dobrý v texte, ale v počítaní občas
    hádže chyby. Presný výpočet radšej necháme obyčajnému kódu.

    Vzorec: 1 palec = 25,4 mm, a dpi hovorí, koľko pixelov sa zmestí na 1 palec.
    Teda: milimetre = pixely / dpi * 25,4
    Príklad: 1920 px pri 300 dpi = 1920 / 300 * 25,4 = 162,56 mm
    """
    return pixely / dpi * 25.4


# ---------------------------------------------------------------------------
# POPIS NÁSTROJA pre LLM.
# Model funkciu px_na_mm nevidí a nevie ju spustiť. Dostane len tento popis, čosi
# ako "jedálny lístok": ako sa volá, na čo je a aké hodnoty od neho chce.
# Podľa popisu sa rozhodne, či ju treba použiť. Preto musí byť popis jasný.
# ---------------------------------------------------------------------------
POPIS_NASTROJA = {
    "name": "px_na_mm",
    "description": "Prepočíta rozmer z pixelov na milimetre pre dané rozlíšenie v dpi.",
    "parameters": {
        "type": "object",
        "properties": {
            "pixely": {"type": "number", "description": "Rozmer v pixeloch, napr. 1920"},
            "dpi": {"type": "number", "description": "Rozlíšenie v dpi, napr. 300"},
        },
        "required": ["pixely", "dpi"],  # bez oboch hodnôt sa nedá počítať
    },
}


# Zoznam nástrojov, ktoré naozaj vieme spustiť: názov, ktorý povie model -> naša funkcia.
# Model napíše len názov (text), a podľa tohto zoznamu nájdeme, ktorú funkciu spustiť.
NASTROJE = {"px_na_mm": px_na_mm}


# ---------------------------------------------------------------------------
# HLAVNÝ PROGRAM
# ---------------------------------------------------------------------------
def main() -> None:
    # Prečíta .env a dá jeho obsah k dispozícii ako "premenné prostredia".
    load_dotenv()

    # Vytiahne kľúč. Ak ho tam niet, spadneme hneď s jasnou správou,
    # nie až neskôr s nejakou zmätočnou chybou od Googlu.
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key or api_key == "SEM_VLOZ_KLUC":
        raise SystemExit("Chýba GEMINI_API_KEY. Vlož ho do súboru .env (pozri README).")

    # "Klient" je spojenie s Gemini. Cez neho posielame otázky.
    # Gemini občas odpovie 503 "som preťažený, skús neskôr". Namiesto toho, aby
    # skript spadol, ho necháme až 6-krát po sebe zopakovať otázku (s pauzami).
    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(retry_options=types.HttpRetryOptions(attempts=6)),
    )

    # KROK 4: opýtame sa na vec, kde sa hodí nástroj, a povieme modelu, že ho má.
    otazka = "Koľko milimetrov má obrázok široký 1920 pixelov pri rozlíšení 300 dpi?"
    config = types.GenerateContentConfig(
        tools=[types.Tool(function_declarations=[POPIS_NASTROJA])]
    )
    odpoved = client.models.generate_content(model=MODEL, contents=otazka, config=config)

    # Model teraz NEODPOVIE číslom. Vráti pokyn "zavolaj nástroj". Pozrieme sa naň.
    # odpoved.function_calls je zoznam takýchto pokynov (prázdny, ak model nástroj nechce).
    if not odpoved.function_calls:
        raise SystemExit("Model nástroj nepoužil, odpovedal rovno: " + str(odpoved.text))

    pokyn = odpoved.function_calls[0]
    print("Model žiada nástroj:", pokyn.name)
    print("S hodnotami:", dict(pokyn.args))

    # KROK 5a: nástroj naozaj spustíme u seba v počítači.
    # NASTROJE[pokyn.name] nájde funkciu podľa názvu, ** rozbalí hodnoty od modelu
    # ({"pixely": 1920, "dpi": 300}) do argumentov funkcie, ako keby sme napísali
    # px_na_mm(pixely=1920, dpi=300).
    funkcia = NASTROJE[pokyn.name]
    vysledok = funkcia(**pokyn.args)
    print("Výsledok nástroja:", vysledok, "mm")

    # KROK 5b: výsledok vrátime modelu. Model si nepamätá predošlé volanie, takže mu
    # pošleme celý rozhovor odznova, v tomto poradí:
    #   1. pôvodná otázka (od nás)
    #   2. jeho vlastný pokyn "zavolaj nástroj" (od modelu), poslať ho treba celý
    #      tak, ako prišiel, lebo Gemini 3 si v ňom nesie svoje skryté "poznámky"
    #   3. výsledok nástroja (od nás)
    rozhovor = [
        types.Content(role="user", parts=[types.Part(text=otazka)]),
        odpoved.candidates[0].content,
        types.Content(
            role="user",
            parts=[
                types.Part.from_function_response(
                    name=pokyn.name,
                    response={"vysledok_mm": vysledok},
                )
            ],
        ),
    ]
    finalna = client.models.generate_content(model=MODEL, contents=rozhovor, config=config)

    # Model má teraz všetko, čo potrebuje, a odpovie normálnou vetou.
    print("\nFinálna odpoveď modelu:", finalna.text)


# Táto podmienka znamená: spusti main() len keď súbor spúšťame priamo
# (uv run main.py), nie keď ho niekto iný importuje ako knižnicu.
if __name__ == "__main__":
    main()
