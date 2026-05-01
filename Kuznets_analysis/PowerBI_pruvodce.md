# Power BI — Průvodce vizualizací EKC projektu

## Přehled

V tomto průvodci vytvoříme v Power BI interaktivní dashboard s těmito vizualizacemi:

| Vizualizace | Výzkumná otázka | Typ grafu |
|---|---|---|
| EKC scatter plot s regresní křivkou | Q1: Vztah HDP–lesy | Scatter chart + Line chart |
| Sloupcový graf příjmových skupin | Q1: Průměrná změna lesa | Clustered bar chart |
| Sloupcový graf podle regionů | Q2: Regionální srovnání | Clustered bar chart |
| Mapa světa — změna lesa | Přehled | Filled map |
| Tabulka "paradoxů" | Q3: Výjimky | Table |

> ⏱️ **Odhadovaný čas**: 2–3 hodiny pro celý dashboard

---

## Část 0: Než začneš

### Instalace Power BI Desktop

1. Otevři prohlížeč a jdi na `https://powerbi.microsoft.com/desktop`
2. Klikni na **Download free** → spustí se stažení instalátoru
3. Spusť instalátor a postupuj podle průvodce (vše defaultní)
4. Power BI Desktop je **zdarma**, nevyžaduje přihlášení pro základní práci

### Příprava dat v Pythonu

Před otevřením Power BI spusť **Notebook 02** (`02_statistika_ekc.ipynb`), který vytvoří tyto soubory:

```
Kuznets_analysis/output/
├── ekc_analysis.csv           ← hlavní dataset (199 zemí)
├── ekc_regression_curve.csv   ← 100 bodů pro EKC křivku
├── regional_summary.csv       ← souhrn podle regionů (7 regionů)
├── outliers.csv               ← paradoxní země (14 zemí)
└── outliers_with_policy.csv   ← paradoxní země + lesní politika
```

> ✅ **Ověř** že soubory existují v Průzkumníku souborů před spuštěním Power BI.

---

## Část 1: Spuštění a orientace v Power BI Desktop

### Krok 1: Spuštění Power BI Desktop

1. Spusť **Power BI Desktop** z nabídky Start nebo plochy
2. Pokud se zobrazí uvítací okno (splash screen), klikni na **X** pro jeho zavření

**Co uvidíš po tomto kroku:**
Hlavní okno Power BI s třemi ikonami vlevo:
- 📊 **Report** (graf) — tady budeš tvořit vizualizace
- 🗄️ **Data** (tabulka) — tady vidíš načtená data
- 🔗 **Model** (propojení) — tady propojuješ tabulky

Nahoře je pás karet podobný Excelu.

---

## Část 2: Načtení dat do Power BI

### Krok 2: Import CSV souborů

Budeš importovat 4 soubory. Postup pro každý je stejný:

1. Na pásu karet klikni na záložku **Home** (Domů)
2. Klikni na tlačítko **Get Data** (Načíst data) — má ikonu databáze
3. Z menu vyber **Text/CSV**
4. V okně pro výběr souboru naviguj do složky `Kuznets_analysis/output/`
5. Vyber soubor → klikni **Open** (Otevřít)

**Co uvidíš po kroku 5:**
Otevře se náhledové okno s několika prvními řádky souboru. Uvidíš, jak Power BI rozpoznal sloupce.

6. Zkontroluj, že data vypadají správně (záhlaví sloupců jsou v prvním řádku)
7. Klikni **Load** (Načíst)

**Co uvidíš po kroku 7:**
Soubor se načte a zavře. Vpravo v panelu **Fields** (Pole) přibude nová tabulka s ikonou tabulky.

Zopakuj kroky 1–7 pro všechny 4 soubory:
- `ekc_analysis.csv`
- `ekc_regression_curve.csv`
- `regional_summary.csv`
- `outliers.csv`

> ⚠️ **Pokud se nezobrazí záhlaví sloupců**: V náhledovém okně klikni na **Transform Data** místo Load. V Power Query editoru klikni na **Use First Row as Headers** (ikona tabulky se šipkou nahoru). Pak **Close & Apply**.

### Krok 3: Kontrola datových typů (Power Query Editor)

Power BI někdy špatně odhadne datový typ sloupce. Je potřeba to zkontrolovat:

1. Na pásu karet klikni **Transform Data** (Transformovat data)
2. Otevře se **Power Query Editor** — nové okno s tabulkovým zobrazením dat
3. Pro každou tabulku (vlevo v panelu **Queries**) zkontroluj ikony u názvů sloupců:
   - `ABC` = text ✓ pro `country`, `code`, `income_group`, `region`
   - `1.2` = desetinné číslo ✓ pro `forest_change`, `mean_gdp`, `log_gdp`, `forest_pred`
4. Pokud je typ špatný: klikni na ikonu vlevo od názvu sloupce → vyber správný typ
5. Po kontrole všech tabulek klikni **Close & Apply** (vlevo nahoře, velké zelené tlačítko)

**Co uvidíš po Close & Apply:**
Power Query Editor se zavře a vrátíš se do hlavního okna. Vpravo dole uvidíš indikátor načítání. Počkej, než skončí.

---

## Část 3: Datový model (propojení tabulek)

### Krok 4: Vytvoření relací

Power BI potřebuje vědět, jak tabulky spolu souvisí — aby filtry fungovaly správně.

1. Klikni na ikonu **Model** (propojení, třetí ikona vlevo)

**Co uvidíš:**
Zobrazení se čtyřmi obdélníky (tabulkami). Mezi nimi mohou být automaticky vytvořené spojovací čáry — nebo žádné.

2. Vytvoř relaci `ekc_analysis` ↔ `outliers`:
   - Přetáhni sloupec **`code`** z tabulky `ekc_analysis`
   - Přesuň ho na sloupec **`code`** v tabulce `outliers`
   - Pustit (drag & drop)
   
**Co uvidíš:**
Zobrazí se dialog **Create relationship** s výběrem sloupců. Ověř, že jsou vybrány správné sloupce (`code` ↔ `code`), pak klikni **OK**.

Mezi oběma tabulkami se objeví tenká čára s čísly `1` a `*` — to označuje relaci One-to-Many.

> ℹ️ Ostatní tabulky (`ekc_regression_curve`, `regional_summary`) v tomto projektu nepotřebují relaci — každá slouží pro samostatnou vizualizaci.

---

## Část 4: Vizualizace

Přejdi do zobrazení **Report** (první ikona vlevo — ikona grafu).

Vpravo vidíš dva panely:
- **Visualizations** (Vizualizace) — ikony různých typů grafů
- **Fields** (Pole) — seznam tabulek a jejich sloupců

Prázdná bílá plocha uprostřed je tvoje plátno (canvas) — sem budeš přidávat vizualizace.

---

### Vizualizace 1: EKC Scatter plot (Q1)

**Co zobrazuje**: Vztah mezi HDP a změnou plochy lesa. Každý bod = jedna země.

#### Část A: Scatter plot

1. Klikni na prázdné místo na plátně (ujisti se, že nic není vybráno)
2. V panelu **Visualizations** klikni na ikonu **Scatter chart** (dvě osy s body — připomíná rozptýlené tečky)

**Co uvidíš:**
Na plátně se vytvoří prázdný šedý rámeček.

3. V panelu **Fields** rozevři tabulku `ekc_analysis` (kliknutím na šipku ▶)
4. Nastav pole přetažením nebo zaškrtnutím:
   - **X axis** (Osa X): přetáhni `log_gdp`
   - **Y axis** (Osa Y): přetáhni `forest_change`
   - **Details** (Podrobnosti): přetáhni `country` — každý bod bude jedna země
   - **Legend** (Legenda): přetáhni `income_group` — skupiny budou mít různé barvy

**Co uvidíš:**
Graf se zaplní ~199 barevnými body. Legenda vpravo nebo dole ukáže 4 barvy pro 4 příjmové skupiny.

> ⚠️ **Pokud vidíš jen 4 velké body místo 199 malých**: Sloupce na osách X/Y jsou nastaveny jako agregát. Klikni na jméno pole v X axis → z menu vyber **Don't summarize** (Neshrňovat). Totéž pro Y axis.

5. Přejmenuj osy pro přehlednost:
   - Klikni na ikonu **Format** (štětec) v panelu Visualizations
   - Rozevři **X axis** → do pole **Title** napiš: `log(HDP na obyvatele)`
   - Rozevři **Y axis** → do pole **Title** napiš: `Změna % lesa (1990–2025)`

6. Přidej referenční čáru y=0 (červená linie odděluje zalesňování od odlesnění):
   - V panelu Format klikni na **Analytics** (ikona lupy)
   - Klikni na **Constant line** → **+ Add**
   - Nastav **Value** (Hodnota) = `0`
   - Nastav barvu: červená nebo šedá, styl: čárkovaně

#### Část B: EKC regresní křivka (přidání k scatter plotu)

Power BI neumí vykreslit polynomiální křivku přímo. Použijeme předpočítané body z Pythonu:

1. Klikni na **prázdné místo** na plátně (ne na scatter plot) — vytvoříme nový vizuál
2. Vyber **Line chart** (čárový graf — ikona s linií)
3. Nastav pole z tabulky `ekc_regression_curve`:
   - **X axis**: `log_gdp_fit`
   - **Y values**: `forest_pred`
4. V panelu Format:
   - Nastav barvu čáry: červená
   - Tloušťka: 3px
   - Odeber tečky (Markers): vypni
5. Přesuň tento line chart na scatter plot tak, aby se překrývaly (drag & drop)
6. Srovnej osy — obě musí mít stejný rozsah na ose X

**Co uvidíš:**
Scatter plot s barevnými body zemí a červenou kvadratickou křivkou ve tvaru ∩. Bod zlomu (vrchol křivky) odpovídá ~$54 885 HDP/os.

---

### Vizualizace 2: Sloupcový graf příjmových skupin (Q1)

**Co zobrazuje**: Průměrná změna lesa v každé příjmové skupině. Měly by být viditelné rozdíly.

1. Klikni na prázdné místo na plátně
2. Vyber **Clustered bar chart** (vodorovný sloupcový graf)
3. Nastav pole z `ekc_analysis`:
   - **Y axis**: `income_group`
   - **X axis**: `forest_change` — Power BI automaticky vypočítá průměr
4. Ověř, že X axis je nastaven na **Average** (Průměr):
   - Klikni na `forest_change` v poli X axis → vyber **Average**
5. Seřaď skupiny od Low po High income:
   - Klikni na `income_group` v Y axis → **Sort by column** → vyber pořadí ručně nebo přidej pomocnou tabulku
6. Přidej referenční čáru x=0:
   - Format → Analytics → Constant line → Value = 0

**Očekávaný výsledek**: High income bude jediná skupina vpravo od nuly (kladná průměrná změna lesa).

---

### Vizualizace 3: Regionální sloupcový graf (Q2)

**Co zobrazuje**: Průměrná změna lesa podle světového regionu.

1. Klikni na prázdné místo na plátně
2. Vyber **Clustered bar chart**
3. Nastav pole z tabulky `regional_summary`:
   - **Y axis**: `region`
   - **X axis**: `mean_change`
4. Přidej **Data labels** (popisky hodnot):
   - Format → Data labels → zapni (On)
5. Seřaď sestupně: klikni na "..." v pravém horním rohu grafu → **Sort descending** → `mean_change`

**Bonus — chybové úsečky (standard deviation)**:
6. Format → Error bars
7. Upper bound: `std_change`, Lower bound: `-std_change` (záporné std)

---

### Vizualizace 4: Mapa světa — Změna lesa

**Co zobrazuje**: Geografické rozložení odlesnění/zalesnění v barvách.

1. Klikni na prázdné místo na plátně
2. Vyber **Filled Map** (chloropleth mapa — ikona s barevnými oblastmi)

> ⚠️ **Pokud Filled Map chybí v panelu Visualizations**: Jdi na **File → Options → Security** → zapni **Map and Filled Map visuals**.

3. Nastav pole z `ekc_analysis`:
   - **Location** (Místo): přetáhni `code` (ISO3 kód, např. CZE) — **NE `country`**, kódy jsou spolehlivější než názvy
   - **Color saturation** (Intenzita barvy): přetáhni `forest_change`

**Co uvidíš:**
Světová mapa, kde tmavší zelená = zalesnění, tmavší červená = odlesnění.

4. Nastav barevnou škálu:
   - Format → Colors → nastav **Minimum**: červená, **Center**: bílá/žlutá, **Maximum**: zelená
   - Center value: `0` (bod rozdílu zalesňování/odlesnění)

> ⚠️ **Pokud mapa nerozpoznává země**: Zkontroluj datový typ sloupce `code` — musí být **Text**. Pokud Power BI zobrazuje chybu "Location not found", zkus místo ISO3 kódu použít sloupec `country`.

---

### Vizualizace 5: Tabulka "Paradoxů" (Q3)

**Co zobrazuje**: Bohaté země které odlesňují + chudé země které zalesňují.

1. Klikni na prázdné místo na plátně
2. Vyber **Table** (tabulka — ikona mřížky)
3. Přidej sloupce z `outliers`:
   - `country`, `income_group`, `region`, `forest_change`, `mean_gdp`, `outlier_category`
4. Nastav podmíněné formátování pro `forest_change`:
   - Klikni na `forest_change` v panelu Fields (při vybraném vizuálu) → **Conditional formatting** → **Background color**
   - Záporné hodnoty: červená, kladné: zelená, střed: bílá
5. Seřaď podle `forest_change` vzestupně (největší odlesňovatelé nahoře)

---

## Část 5: Dashboard — Sestavení stránky

### Krok: Přidání nadpisu

1. Na pásu karet klikni **Insert** → **Text box** (textové pole)
2. Napiš: `Environmental Kuznets Curve — Analýza lesů a HDP 1990–2025`
3. Nastav velikost písma: 18–20, tučné

### Krok: Layout dashboardu

Přesuň a změň velikost vizualizací na plátně:

```
┌─────────────────────────────────────────────────────────────┐
│  NADPIS: Environmental Kuznets Curve — Analýza lesů         │
├──────────────────────┬──────────────────────────────────────┤
│  SCATTER PLOT        │  SLOUPCOVÝ GRAF                      │
│  + EKC křivka        │  Příjmové skupiny                    │
│  (log_gdp vs         │  (income_group vs forest_change)     │
│   forest_change)     │                                      │
├──────────────────────┴──────────────────────────────────────┤
│  MAPA SVĚTA — Změna lesa 1990–2025                          │
├──────────────────────┬──────────────────────────────────────┤
│  SLOUPCOVÝ GRAF      │  TABULKA PARADOXŮ                    │
│  Regiony (Q2)        │  Q3: Výjimky z EKC teorie            │
└──────────────────────┴──────────────────────────────────────┘
```

### Krok: Přidání filtrů (Slicers)

Slicer = interaktivní filtr — umožní přepínat mezi skupinami zemí.

1. Klikni na prázdné místo
2. Vyber **Slicer** (ikona filtru — čtverec s hranatými závorkami)
3. Přetáhni `income_group` z `ekc_analysis` do pole **Field**
4. Format → Slicer settings → nastav **Selection** na **Multi-select** (výběr více hodnot)
5. Přidej druhý Slicer pro `region`

**Co uvidíš:**
Dva filtrovací panely. Po kliknutí na skupinu (např. "High income") se všechny grafy automaticky přefiltrují.

### Krok: Tooltip pro scatter plot

Tooltip = co se zobrazí při najetí myší na bod v grafu.

1. Klikni na scatter plot
2. V panelu Visualizations přejdi do záložky **Fields**
3. Do pole **Tooltips** přetáhni: `country`, `income_group`, `region`, `forest_1990`, `forest_2025`

---

## Část 6: Připojení k SQL Serveru (bonus)

Pokud jsi splnila Notebook 03 (SQL bonus) a data jsou v databázi:

1. **Home → Get Data → SQL Server**
2. Zadej **Server**: `localhost` (nebo název serveru)
3. Zadej **Database**: `EKC_Analysis`
4. Klikni **OK** → v okně Navigator zaškrtni tabulky: `ekc_analysis`, `regional_summary`, `outliers`
5. Klikni **Load**

> Výhoda: Data se aktualizují automaticky po spuštění Python skriptu.

---

## Část 7: Uložení a sdílení

1. **File → Save As** → ulož jako `.pbix` soubor do složky projektu
2. Pro sdílení s mentory: **File → Export → Export to PDF** (nevyžaduje Power BI licenci pro příjemce)

---

## Nejčastější chyby začátečníků

Zde jsou chyby, které se nejčastěji stávají — a jak je opravit:

### 1. Scatter plot zobrazuje 4 velké body místo 199 malých

**Příčina**: Power BI agreguje hodnoty (sčítá nebo průměruje) místo aby zobrazoval individuální body.

**Oprava**:
- Klikni na pole v **X axis** → z menu vyber **Don't summarize**
- Klikni na pole v **Y axis** → z menu vyber **Don't summarize**
- Ujisti se, že v poli **Details** je nastaveno `country` (každý bod = jedna země)

### 2. Mapa nezobrazuje správné země

**Příčina**: Power BI nerozpoznává české/anglické názvy zemí nebo má jiný formát.

**Oprava**:
- Místo sloupce `country` použij sloupec `code` (ISO3 kód, např. CZE, BRA, DEU)
- Ověř datový typ `code` — musí být **Text** (ne číslo)
- Klikni na **Location** pole → z menu vyber **Country** jako kategorii dat

### 3. CSV soubor se nenačte správně (špatné sloupce, diakritika)

**Příčina A**: Power BI špatně dělí sloupce (čárka vs. středník jako oddělovač).

**Oprava A**: V náhledovém okně při importu klikni **Transform Data**. V Power Query nahoře klikni **View → Query Settings** a zkontroluj delimiter. Nebo: **Home → Split Column → By Delimiter**.

**Příčina B**: Diakritika (háčky, čárky) se zobrazuje jako otazníky nebo čtverce.

**Oprava B**: Data z Pythonu jsou exportována s `encoding='utf-8-sig'` — Power BI to zvládne. Pokud přesto vidíš chyby, v Power Query klikni na **Source** v levém panelu a změň encoding na `UTF-8`.

### 4. Box and Whisker chart chybí v panelu Visualizations

**Příčina**: Power BI Desktop nemá box plot ve výchozí instalaci.

**Oprava**:
1. V panelu Visualizations klikni na tři tečky **"..."** → **Get more visuals** (Získat další vizuály)
2. Vyhledej **"Box and Whisker"** od Daniel Marsh-Patrick
3. Klikni **Add** → vizuál se přidá do panelu
4. Pokud nejde přidat (firemní politika): použij místo toho **Clustered bar chart** s průměrem.

### 5. Hodnoty v grafu jsou součty místo průměrů

**Příčina**: Power BI defaultně sčítá numerické hodnoty.

**Oprava**: Klikni na pole v panelu Fields (při vybraném vizuálu) → z rozbalovacího menu vyber **Average** místo **Sum**.

### 6. Relace mezi tabulkami nefunguje (filtry neovlivňují jiné vizualizace)

**Příčina**: Tabulky nejsou propojeny přes sloupec `code`.

**Oprava**:
1. Přejdi do zobrazení **Model** (ikona propojení vlevo)
2. Ověř, že mezi `ekc_analysis` a `outliers` je čára
3. Pokud ne: přetáhni `code` z jedné tabulky na `code` druhé
4. Zkontroluj, že oba sloupce mají typ **Text** (ne číslo)

### 7. Scatter plot nezobrazuje regresní křivku

**Příčina**: Line chart pro EKC křivku má jiný rozsah osy X než scatter plot.

**Oprava**:
1. Klikni na Line chart → Format → X axis
2. Nastav **Minimum** a **Maximum** stejně jako na scatter plotu
3. Oba grafy musí být umístěny přesně na sobě (overlay)

---

## Slovníček pojmů v Power BI

| Anglicky | Česky | Kde to najdeš |
|---|---|---|
| Get Data | Načíst data | Záložka Home |
| Transform Data | Transformovat data | Záložka Home |
| Load | Načíst | Tlačítko v náhledovém okně |
| Close & Apply | Zavřít a použít | Power Query Editor, vlevo nahoře |
| Visualizations pane | Panel vizualizací | Vpravo, ikony grafů |
| Fields pane | Panel polí | Vpravo, seznam tabulek |
| Format pane | Panel formátování | Vpravo, ikona štětce |
| Analytics pane | Panel analytiky | Vpravo, ikona lupy |
| Slicer | Filtr / Průřez | V panelu Visualizations |
| Measure | Míra (výpočet v DAX) | Pokročilé — zatím nepotřebuješ |
| Drill down | Přejít do detailu | Kliknutí na bod v grafu |
| Don't summarize | Neshrňovat | Menu u pole na ose |
| Conditional formatting | Podmíněné formátování | Format → buňka |
