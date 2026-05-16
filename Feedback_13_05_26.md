# Code review — kveten 2026

Prošel jsem celé `scripts/` a musím říct, že jste udělaly hodně dobré práce. Níže jsou věci, které stojí za pozornost — od chyb, na které by se mělo podívat, po moje poznámky, které jsou spíš k zamyšlení nebo pro informaci.

---

## Ve "zkoušecím" notebooku chybí year v merge klíči — ale ve finální analýze je to správně — Kristina

### [`python_connect_db.ipynb`](scripts/statistics/python_connect_db.ipynb) — merge bez roku dělá Cartesian product

V tomto notebooku je merge takhle:

```python
df = pd.merge(df_forest, df_gdp, on=["country_code"])
```

Chybí `"year"` jako druhý join klíč. Pandas to interpretuje tak, že každý řádek pro danou zemi z `fact_forest` spáruje s **úplně každým** řádkem pro stejnou zemi z `fact_gdp`. Afghánistán má 35 řádků v každé tabulce — výsledek je 35 × 35 = 1225 řádků místo 35.

Není to jen teoretický problém — ve výstupu notebooku to jde přímo vidět. Řádek 0 je AFG 1990 (forest) + AFG 1990 (GDP), řádek 1 je AFG 1990 (forest) + AFG **1991** (GDP), a tak dál.

V [`Q1-correlation_forest_GDP.ipynb`](scripts/statistics/Q1-correlation_forest_GDP.ipynb) máš merge napsaný správně, takže výsledky analýzy to neovlivňuje. Ale `python_connect_db` by jako ukázkový notebook měl být správně.

**Případná Oprava:**
```python
df = pd.merge(df_forest, df_gdp, on=["country_code", "year"])
```

---

## Statistická interpretace — Kristina

### [`Q1-correlation_forest_GDP.ipynb`](scripts/statistics/Q1-correlation_forest_GDP.ipynb) — kvadratický člen není až tak průkazný

V OLS výsledcích je tenhle řádek:

```
np.power(np.log(gdp_per_capita), 2)   coef = -0.0108   P>|z| = 0.051
```
GDP per capita má statisticky průkazný vliv na změnu lesní plochy (lineární člen p = 0.017). Kvadratický člen, který by potvrzoval EKC tvar obrácené U, je na hranici průkaznosti (p = 0.051) — výsledek naznačuje tento tvar, ale není 100% průkazný, proto by bylo alespoň dobré vědět, že turning point ~56 000 USD je spíš orientační číslo než pevný bod.

Neznamená to, že je to uděláno špatně, ale výsledek by měl být formulovaný lehce opatrněji, třeba:

> *"Kvadratický člen je na hranici statistické významnosti (p = 0.051), výsledek je tedy třeba interpretovat opatrně. Pokud by model platil, turning point by byl přibližně 56 000 USD — to je úroveň, které dosahuje jen asi 20 % zemí v datasetu."*

Tabulka s výsledky modelu je správná, každopádně vizualizace (scatter plot?) bude při prezentaci snad přesvědčivější.

---

## Datová kvalita — Barbara -> FIXED (pridaný koment, aby to bolo v dokumente jasné)

### Tři věci v databázi, které stojí za zkontrolování nebo opravu

**1. `fact_forest` sahá do 2025, `fact_gdp` jen do 2024**

V [`03_fact_tables.ipynb`](scripts/database/03_fact_tables.ipynb) to jde vidět ve verifikačním dotazu:
```
fact_forest: 1990–2025
fact_gdp:    1990–2024
```

Při joinu obou tabulek se řádky za rok 2025 tiše ztratí — žádná chyba, ale potenciálně matoucí, dobré na to myslet.

**2. Grónsko je vyloučeno z analýzy subregionů, ale ne z regionů** -> FIXED (vyradený z regiónov taktiež + koment v dokumentácii prečo)

V [`Statistics_accross_subregions.ipynb`](scripts/statistics/Statistics_accross_subregions.ipynb):
```python
df_europe = df_europe[df_europe["country_code"] != "GRL"]
```

Proč je Grónsko specificky vyřazené? Pokud jde o outliera, měl by být vyloučen konzistentně ve všech noteboocích — nebo by mělo být v kódu vysvětleno, proč jen tady. Nebo to aspoň řekněte mně, protože mě to zajímá :)

**3. Zvláštní kombinace region × subregion v `dim_country`** -> FIXED (nevyžaduje zmenu, je to zámerné, pretože sú to edge cases od WB.)

Ve verifikačním dotazu v [`02_dim-tables.ipynb`](scripts/database/02_dim-tables.ipynb) jsou tyhle kombinace:

| Region | Subregion | Počet zemí |
|--------|-----------|------------|
| Middle East & North Africa | Eastern and Southern Africa | 1 |
| Europe & Central Asia | North America | 1 |
| North America | Caribbean | 1 |

Stojí za to zjistit, o které země jde a jestli jde o chybu ve zdrojovém mapping souboru nebo jde o záměrnou klasifikaci. Výsledky analýzy to pravděpodobně neovlivní, ale je dobré to mít zmapované.

## RESPONSE: 
All three are World Bank classification edge cases, not mapping errors. Greenland was excluded from subregion analysis specifically because its region/subregion combination (Europe & Central Asia / North America) makes it an outlier that would distort European subregion statistics. It remains included in regional analysis under Europe & Central Asia.

---

## Kvalita kódu

### Špatný import matplotlib — Kristina ([`Q1-correlation_forest_GDP.ipynb`](scripts/statistics/Q1-correlation_forest_GDP.ipynb))

```python
import matplotlib as plt        # špatně
import matplotlib.pyplot as plt # správně
```

Samo o sobě ničemu nevadí, ale kdybys zkoušela vizualizaci EKC křivky, narazíš na chybu.

---

### Řádkový UPDATE místo hromadného — Barbara ([`Add foest_change_pct_column.ipynb`](scripts/database/Add%20foest_change_pct_column.ipynb)) 

```python
for index, row in df_update.iterrows():
    conn.execute(text("UPDATE dbo.fact_forest SET ..."), {...})
```

Takhle se spustí ~7 500 individuálních SQL dotazů jeden po druhém. Funguje to (a výsledek je správný), ale je to pomalé a v praxi je to anti-pattern. Pokud vás zajímá jak to udělat lépe, podívejte se na `executemany()` nebo přístup přes dočasnou tabulku a jeden UPDATE JOIN. Ale v rámci tohoto projektu bych to neřešil.

---

### Překlepy v názvech souborů — Barbara -> FIXED

- [`Add foest_change_pct_column.ipynb`](scripts/database/Add%20foest_change_pct_column.ipynb) → správně `forest`
- [`Statistics_accross_subregions.ipynb`](scripts/statistics/Statistics_accross_subregions.ipynb) → správně `across`

Malá věc, ale tyhle soubory jsou commitnuté do gitu a přejmenování bude potřeba řešit přes `git mv`.

---

## Co se povedlo

Databáze je postavená dobře. Rozdělení na `raw` a `dbo` schéma dává smysl, dimenzionální model funguje a join přes všechny tři tabulky v [`03_fact_tables.ipynb`](scripts/database/03_fact_tables.ipynb) dává správný výsledek. AGG_ prefix pro entity bez ISO3 kódu (EU, Anglie...) je fajn řešení — neztrácí se data a je hned jasné co to je.

Statistická část má ve všech noteboocích konzistentní strukturu — hypotéza, test normality, správný test, interpretace. To se mi líbí.

Income groups analýza je asi nejpřesvědčivější část projektu — to "schodiště" od nejchudších zemí (−0.15 % ročně) po nejbohatší (+0.03 %) je jasné, dobře interpretované a přirozeně navazuje na EKC hypotézu. A subregionální drill-down do Evropy je dobrý nápad na rozšíření.

Jen tak dál :)
