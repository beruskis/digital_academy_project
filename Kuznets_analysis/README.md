# Kuznetova ekologická křivka (EKC) — Analýza lesů a HDP

## O projektu

Tento projekt zkoumá tzv. **Environmental Kuznets Curve (EKC)** — teorii, která říká:

> Chudé země při ekonomickém růstu kácejí lesy, ale po překročení určité hranice bohatství se trend otočí a země začínají lesy obnovovat.

Analyzujeme data **235 zemí za období 1990–2025** a ptáme se:

| # | Výzkumná otázka | Hypotéza |
|---|---|---|
| **Q1** | Existuje měřitelný vztah mezi HDP a změnou plochy lesa? | Ekonomicky vyspělejší státy vykazují kladný přírůstek zalesněné plochy |
| **Q2** | Záleží na regionu více než na HDP? | Ano — region a politika jsou silnějšími prediktory než samotný příjem |
| **Q3** | Které bohaté země odlesňují a které chudé zalesňují — a proč? | Výjimky ukazují na vliv politiky a hustoty obyvatelstva |

---

## Použité nástroje a data

| Nástroj | K čemu |
|---|---|
| **Python + pandas** | Načtení, čištění a spojení dat, statistické výpočty |
| **scipy.stats** | Korelace, testy hypotéz |
| **numpy** | Polynomiální regrese, výpočet bodu zlomu |
| **Power BI** | Vizualizace: scatter plot, box chart, mapa, EKC křivka |
| **SQL Server** *(bonus)* | Uložení dat do databáze, SQL dotazy |

### Datové soubory

Všechna vstupní data jsou ve složkách `../data_dan/` a `../data_raw/`:

| Soubor | Popis |
|---|---|
| `data_dan/forest_ekc_model.csv` | Změna plochy lesa (%) 1990–2025 po zemích |
| `data_dan/MAIN_Forest_GDP_joined.csv` | Panelová data: % lesního pokryvu + HDP po zemích a letech |
| `data_raw/2025_World_Bank_classification_by_Income.csv` | Klasifikace zemí dle příjmu + region (Světová banka) |
| `data_raw/Forest_share_1990_2025.csv` | % lesního pokryvu 1990 a 2025 |

---

## 2 styly učení — vyber si svůj!

```
Kuznets_analysis/
├── A_ulohy/           ← VÝZVA: prázdné buňky, nápovědy, + řešení zvlášť  
└── B_kombinovane/     ← NEJLEPŠÍ KOMPROMIS: ukázka vzoru → tvůj úkol
```

### Jak si vybrat?

**A — Úlohy (Samostatná práce)**
- Dostaneš zadání + nápovědu, kód napíšeš sama
- Řešení je v souboru `*_RESENI.ipynb` — otevři ho až po vlastním pokusu!
- Ideální pokud: chceš si co nejvíce vyzkoušet

**B — Kombinované (Ukázka + Tvůj tah)**
- Každý nový koncept: nejprve ukázka na jiných datech, pak ty zkusíš analogický úkol
- Ideální pokud: chceš se učit z příkladů, ale zároveň procvičovat

---

## Srovnání variant z pohledu studentky

> Obě varianty vedou ke **stejným výsledkům a stejným výstupním souborům**. Liší se jen mírou opory při psaní kódu.

### Co tě čeká v každé variantě

| | Varianta A — Úlohy | Varianta B — Kombinované |
|---|---|---|
| **Počet notebooků** | 2 × pár (ULOHY + RESENI) | 2 notebooky |
| **Kód píšeš** | od nuly (s nápovědou) | po vzoru z UKÁZKY |
| **Záchranná síť** | RESENI notebook hned vedle | UKÁZKA je přímo nad tvým úkolem |
| **Obtížnost** | vyšší — musíš vymyslet strukturu | nižší — vzor vidíš hned |
| **Co se naučíš navíc** | číst chyby, ladit kód sám/a | rozpoznávat vzory a aplikovat je |
| **Přeskočení** | možné — ale RESENI spusť vždy | možné — UKÁZKA funguje samostatně |

### Zkušenost z průchodu variantou A

Varianta A čeká se čtyřmi notebooky (NB01 + NB02, každý ve dvou verzích). Nejsilnější moment nastane u **Úlohy 6 (peer-group residuál)** — zadání je podrobné, ale propojení tří kroků (geografický filtr → mediány skupin → klasifikace) vyžaduje soustředění. Záchranná síť je vždy k dispozici: soubor `*_RESENI.ipynb` leží ve stejné složce.

Postup, který funguje: otevři ULOHY, přečti celé zadání jedné úlohy, zkus napsat kód, porovnej výstup s "Očekávaným výstupem" přímo v zadání — a teprve pak, pokud se zasekneš, otevři RESENI.

### Zkušenost z průchodu variantou B

Varianta B pracuje se dvěma notebooky. Každá sekce vypadá stejně: UKÁZKA na jiných datech → tvůj úkol na datech projektu. Největší pomoc je, že vzorový kód vidíš **přímo nad svou buňkou** — stačí ho adaptovat.

⚠️ **Důležité pro Variantu B**: V Notebooku 01 musíš dokončit **sekci Export** (záložka TEĎ TY na konci NB01) dříve než otevřeš Notebook 02. Notebook 02 čte soubor `../output/ekc_analysis.csv` — ten vznikne právě tímto exportem. Bez toho NB02 selže na prvním načtení dat.

Stráže v kódu (`⚠️ Nejdřív dokonči předchozí buňku...`) ti pohlídají závislosti — pokud vidíš takové varování, vrať se o buňku výš a doplň chybějící kód.

### Výsledky, ke kterým obě varianty dospějí

| Analýza | Výsledek |
|---|---|
| Pearsonova korelace (log_gdp vs. forest_change) | r = **0.363**, p < 0.001 |
| EKC bod zlomu (kvadratická regrese) | **$54 885**/os. |
| R² kvadratického modelu | **0.146** (14.6 % variance) |
| Mann-Whitney U test (High vs. Low income) | U = 1594, p < 0.001 → **H1 POTVRZENA** |
| Kruskal-Wallis test (7 regionů) | H = 62.5, p < 0.001 → **REGIONY SE LIŠÍ** |
| Počet paradoxních zemí | **8** (3 bohatí odlesňovatelé + 5 chudých zalesňovatelů) |
| Policy score chudých zalesňovatelů | **3.0/3** (všech 5 zemí: max. skóre) |

---

## Postup projektu

```
Notebook 01          Notebook 02           Power BI
Průzkum dat    →    Statistika & EKC   →  Vizualizace
(pandas)            (korelace, regrese)    (grafy, dashboard)
                         ↓
                    Notebook 03 (bonus)
                    SQL + databáze
```

### Výstupy pro Power BI

Notebook 02 vytvoří tyto soubory do složky `output/`:

| Soubor | Obsah | Použití v Power BI |
|---|---|---|
| `output/ekc_analysis.csv` | Hlavní dataset: země, HDP, les, region, příjmová skupina | Scatter plot, box chart, mapa |
| `output/ekc_regression_curve.csv` | Body polynomiální regresní křivky | EKC křivka |
| `output/regional_summary.csv` | Průměry a mediány podle regionu | Q2 sloupcový graf |
| `output/outliers.csv` | "Paradoxní" země (bohaté kácí, chudé zalesňují) | Q3 analýza |
| `output/outliers_with_policy.csv` | Paradoxní země + lesní politika + peer-residuál | Q3 tabulka, peer-residuál graf, lesní politika |

---

## Požadavky

```bash
pip install pandas numpy scipy matplotlib
# Pro SQL bonus:
pip install pyodbc sqlalchemy
```

---

## Průvodce Power BI

Kompletní návod pro Power BI je v souboru: [PowerBI_pruvodce.md](PowerBI_pruvodce.md)
