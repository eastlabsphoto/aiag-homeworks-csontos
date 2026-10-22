# Úloha 1: LLM, ktorý si zavolá nástroj

## Zadanie

> Napíš Python skript, ktorý zavolá LLM API, použije nástroj (napr. výpočtovú funkciu)
> a vráti odpoveď späť LLM.
>
> Odovzdať: zdrojový kód (ideálne GitHub). Deadline: 23. 11. 2026, max. 100 bodov.

## Zápisník rozhodnutí (ako som rozmýšľal)

Úlohu riešim vibecodingom, takže tu je aj to, čo som rozhodol ja a prečo.

| # | Rozhodnutie | Prečo |
|:--|:--|:--|
| 1 | **Používam Gemini API od Googlu** | Z nejakého dôvodu mám na účte 4 € kreditu. Na túto úlohu to bohato stačí, tak nemusím nikam vkladať kartu. |
| 2 | **Podklady z hodiny beriem z `03_gemini/4_tools`** | Lektor tam ukazuje, ako sa modelu povedia nástroje. Ukáže ale len prvú polovicu (model povie „zavolaj funkciu“), druhá polovica chýba. Tú doplníme. |
| 3 | **API kľúč je v `.env`, ktorý je v `.gitignore`** | Kľúč je ako heslo ku kreditnej karte. Keby sa dostal na GitHub, niekto by mi ním minul kredit. `.env.example` je len prázdna šablóna a tá na GitHub ísť môže. |
| 4 | **Úlohu riešime po krokoch** | Nechcem dostať hotový kód, ktorému nerozumiem. Po každom kroku si overím, že to funguje a že viem vysvetliť prečo. |
| 5 | **Model `gemini-3.7-flash`, nie ten z hodiny** | Lektorov `gemini-2.5-flash` Google pre nových používateľov vypol (chyba 404). Odporúčaný `gemini-3.8-flash` bol preťažený (chyba 503), ostatné som vyskúšal jedným volaním a `3.7-flash` odpovedal spoľahlivo. |
| 6 | **Nástroj: prepočet pixelov na mm podľa DPI** | Je to výpočet, ktorý LLM nemá robiť z hlavy. Rozumiem mu z grafiky a výsledok viem overiť na kalkulačke (1920 px pri 300 dpi = 162,56 mm). |
| 7 | **Nástroj si píšem sám, nepoužívam hotový** | „Nástroj“ je pre LLM vlastná funkcia v mojom skripte, aj lektor to tak ukazuje. Vstavané nástroje Gemini (napr. vyhľadávanie) beží Google u seba, takže by skript nemal čo vrátiť späť modelu, a zadanie chce práve tento obeh. Hotové nástroje cez MCP prídu v ďalšej téme kurzu. |
| 8 | **Automatické opakovanie pri chybe 503** | Gemini je občas preťažený a skript potom po prvom pokuse spadol. Knižka od Googlu vie otázku sama zopakovať, tak som to zapol (až 6 pokusov). Nie je to nič zložité, je to jedno nastavenie pri vytváraní klienta. |

## Ako to celé funguje (po ľudsky)

LLM nevie počítať ani nevie nič spustiť. Vie len písať text. Preto celá vec prebieha ako rozhovor
medzi tromi stranami:

```
 Ja (skript) ──1. otázka + zoznam nástrojov──▶  LLM (Gemini)
 Ja (skript) ◀──2. „zavolaj nástroj X s hodnotami Y“──  LLM
 Ja (skript)  spustí funkciu X(Y) u seba v počítači  → výsledok
 Ja (skript) ──3. „výsledok funkcie je Z“──────▶  LLM
 Ja (skript) ◀──4. finálna odpoveď po ľudsky──────  LLM
```

Prirovnanie: LLM je ako kreatívny riaditeľ, ktorý nevie ovládať Photoshop. Povie grafikovi
„zmenši to na 300 dpi“, grafik to naklikne a povie mu výsledok, a riaditeľ potom klientovi
napíše pekný mail. Skript som v tomto prípade ja, grafik.

Lektorov príklad končí na kroku 2. Úloha chce kroky 3 a 4.

## Stav

- [x] Krok 1: kostra projektu, `.gitignore`, `.env`
- [x] Krok 2: výber nástroja (funkcie, ktorú bude LLM volať)
- [x] Krok 3: prvé volanie Gemini (overenie, že kľúč funguje)
- [x] Krok 4: model požiada o nástroj
- [x] Krok 5: spustíme nástroj a vrátime výsledok modelu
- [x] Krok 6: finálna odpoveď + vyskúšanie a zhrnutie

## Ako to spustiť

1. Skopíruj `.env.example` ako `.env` a vlož svoj kľúč z <https://aistudio.google.com/apikey>.
2. V tomto priečinku spusti:

```bash
uv run main.py
```

## Výsledok

Takto vyzerá skutočný beh skriptu (otázka: koľko mm má obrázok široký 1920 px pri 300 dpi):

```
Model žiada nástroj: px_na_mm
S hodnotami: {'pixely': 1920, 'dpi': 300}
Výsledok nástroja: 162.56 mm

Finálna odpoveď modelu: Obrázok so šírkou 1920 pixelov pri rozlíšení 300 dpi má šírku 162,56 mm (približne 16,26 cm).
```

Číslo 162,56 vypočítala moja funkcia `px_na_mm`, nie model. Model len zistil, že ju treba zavolať,
doplnil do nej čísla z vety a po vrátení výsledku ho napísal ľudsky. Dá sa to overiť na kalkulačke:
1920 / 300 × 25,4 = 162,56.

## Čo môže ísť zle

| Čo vidím | Čo to znamená | Čo robiť |
|:--|:--|:--|
| `Chýba GEMINI_API_KEY...` | V `.env` je ešte `SEM_VLOZ_KLUC` alebo súbor chýba. | Skopírovať `.env.example` ako `.env` a vložiť kľúč. |
| `404 NOT_FOUND ... no longer available` | Google model vypol (stalo sa lektorovmu `gemini-2.5-flash`). | V `main.py` zmeniť `MODEL` na iný z <https://ai.google.dev/gemini-api/docs/models>. |
| `503 UNAVAILABLE ... high demand` | Model je práve preťažený. Nie je to chyba v kóde. | Skript to sám skúša až 6-krát. Ak aj tak padne, spustiť znova o chvíľu alebo zmeniť `MODEL`. |
| `Model nástroj nepoužil, odpovedal rovno` | Model sa rozhodol nezavolať funkciu. | Spustiť znova alebo upraviť otázku, aby bolo jasné, že ide o prepočet. |
| `400 INVALID_ARGUMENT ... API key not valid` | Kľúč v `.env` je zlý (preklep, orezaný, zrušený). | Skontrolovať ho alebo vygenerovať nový v Google AI Studio. |
