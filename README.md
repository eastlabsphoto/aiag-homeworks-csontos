# aiag-homeworks-csontos

Domáce úlohy ku kurzu **Budoucnost je tady: AI agenti**.

## Kto tu programuje (spoiler: nikto)

Som grafik, nie programátor. Kód v tomto repe som sám nenapísal a nebudem predstierať, že áno.
Všetky úlohy riešim cez **vibecoding**: zadanie dám AI asistentovi, ten napíše kód a ja dohliadam
na to, aby to robilo, čo má, a aby som tomu rozumel.

Používam:

- **Claude Code**, ako prvú voľbu,
- **Codex**, keď mi dôjde kvóta v Claude Code (stáva sa to častejšie, než by som chcel).

## Pravidlo č. 1: musí to fungovať aj byť pochopiteľné

Každá úloha musí splniť dve veci naraz:

1. **Spĺňa zadanie.** Funguje, robí to, čo učiteľ chce, a dá sa to overiť.
2. **Rozumiem jej ja, grafik.** Nestačí, že kód prejde. Musím vedieť, čo robí, prečo to tak je
   a čo by sa stalo, keby som to zmenil.

Ak kód funguje, ale nikto okrem AI nechápe prečo, úloha nie je hotová.

## Ako má vyzerať každá úloha

Každá úloha má vlastný priečinok (napr. `01_nazov_ulohy/`) a v ňom vlastné `README.md`.
V tom README musí byť:

- **Čo bolo zadanie**, jednou-dvoma vetami.
- **Čo sme vlastne postavili**, po ľudsky a bez žargónu. Ak sa žargón nedá obísť, hneď sa vysvetlí.
- **Ako to spustiť**, presné príkazy na skopírovanie, aby to zvládol aj učiteľ.
- **Ako to funguje**, krok za krokom. Pomáha prirovnanie z reálneho sveta, ideálne z grafiky
  (vrstvy, export, tlačiareň a podobne).
- **Čo môže ísť zle** a čo vtedy robiť.
- **Slovníček**, ak sa v úlohe objavili nové pojmy.

## Pokyny pre AI asistenta (Claude Code, Codex, hocikto ďalší)

Ak čítaš toto README ako LLM, platí pre teba toto:

1. **Najprv správne, potom pekne.** Kód musí splniť zadanie. Zadanie si prečítaj dvakrát.
   Ak je nejasné, opýtaj sa. Nehádaj.
2. **Komentuj, akoby čítal debil.** Myslí sa tým človek, ktorý nikdy neprogramoval, nie hlúpy človek.
   Teda ja, grafik. Konkrétne:
   - Nad každým súborom napíš, na čo slúži.
   - Nad každou funkciou napíš, čo robí a prečo existuje.
   - Pri každom nie celkom zjavnom riadku napíš, čo sa tam deje.
   - Komentuj **prečo**, nielen **čo**. Zlé: `# pripočíta 1`. Dobré: `# počítame pokusy, aby sme po troch skončili`.
   - Komentáre píš po slovensky, jednoducho, bez skratiek a bez zbytočnej angličtiny.
3. **Vysvetli, než urobíš.** Pred väčšou zmenou povedz, čo ideš robiť a prečo.
   Po zmene povedz, čo sa zmenilo a aké to má dôsledky.
4. **Prirovnania vítané.** Čím viac sa to dá prirovnať k niečomu z bežného sveta alebo z grafiky,
   tým lepšie.
5. **Jednoduché pred šikovným.** Radšej dlhší a zrozumiteľný kód než krátky a vtipný trik.
   Žiadne zbytočné frameworky ani predčasné optimalizácie.
6. **Over, že to funguje.** Spusti to a pozri sa na výsledok. Netvrď „hotovo“ bez dôkazu.
   Ak sa niečo nedalo overiť, povedz to nahlas.
7. **Nič nedelaj potichu.** Nemaž súbory, neprepisuj veci mimo úlohy a nenaťahuj závislosti bez toho,
   aby si mi to povedal.
8. **Každá úloha dostane README.** Podľa sekcie vyššie. Aktualizuj ho spolu s kódom.
9. **Riaď sa aj Karpathyho pravidlami.** Sú v súbore [`CLAUDE.md`](CLAUDE.md) (pre Codex je tam odkaz v
   [`AGENTS.md`](AGENTS.md)). Skrátene: najprv premýšľaj a pýtaj sa, píš čo najmenej kódu,
   mení len to, čo treba, a vždy si stanov, ako overíš, že to funguje.
   Ak sa niečo bije s týmto README, vyhráva toto README (napr. komentárov má byť veľa).

Pravidlá pochádzajú z projektu [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills),
ktorý zhrnul bežné chyby AI pri programovaní do štyroch zásad.

## Vtipná poznámka na záver

Ak sa vám zdá, že komentárov je v kóde viac než samotného kódu, je to zámer.
Ak sa vám zdá, že sú príliš jednoduché, je to tiež zámer.
Grafik s Ctrl+Z je nebezpečný. Grafik s Ctrl+Z a bez komentárov v kóde je úplne stratený.
