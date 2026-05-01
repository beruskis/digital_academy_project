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
├── B_ulohy/           ← VÝZVA: prázdné buňky, nápovědy, + řešení zvlášť  
└── C_kombinovane/     ← NEJLEPŠÍ KOMPROMIS: ukázka vzoru → tvůj úkol
```

### Jak si vybrat?

**B — Úlohy (Samostatná práce)**
- Dostaneš zadání + nápovědu, kód napíšeš sama
- Řešení je v souboru `*_RESENI.ipynb` — otevři ho až po vlastním pokusu!
- Ideální pokud: chceš si co nejvíce vyzkoušet

**C — Kombinované (Ukázka + Tvůj tah)**
- Každý nový koncept: nejprve ukázka na jiných datech, pak ty zkusíš analogický úkol
- Ideální pokud: chceš se učit z příkladů, ale zároveň procvičovat

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
