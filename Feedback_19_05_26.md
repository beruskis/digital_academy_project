# Code review — 19. květen 2026 (2. kolo)

Prošel jsem poslední commity, udělal svoje vlastní review a požádal Clauda o jeho review. Níže je souhr věcí, které jsme společně našli, nějakou část z věcí, které našel Claude a nedávali mi až tolik smysl nebo potřebu už jsem promazal, zároveň jsem se se snažil připsat i můj názor k těmto jeho bodům. 

Nicméně samotná implementace a zapracování nějakých myšlenek už bude na vás a vašem rozhodnutí, co vnímáte jako přínosné :) 

---

## Chybí kód pro Mann-Whitney pairwise test

### [`Statistics_income_groups.ipynb`](scripts/statistics/Statistics_income_groups.ipynb) — závěr v textu, kód chybí

V markdown buňce je napsáno:

> *"Mann-Whitney confirmed that all pairs are significantly different from each other."*

#### tohle mě trochu zmátlo, protože jsem to nikde nenašel, tak jsem na to požádal AI o průzkum projektu:
Žádná code buňka tento test nespouští — ani v tomto notebooku, ani jinde v projektu. Výsledek je tedy jen tvrzení v textu, bez kódu a výstupu, který by ho podložil. Pokud notebook někdo spustí od začátku, toto tvrzení není ověřitelné.

V [`Statistics_across_regions.ipynb`](scripts/statistics/Statistics_across_regions.ipynb) je to uděláno správně — vybraly jste konkrétní páry s odůvodněním a ke každému spustily Mann-Whitney. Stejný přístup stačí i tady: nemusíte testovat všech 6 kombinací, ale aspoň 2–3 páry s výstupem. Pro income groups by zajímavé páry mohly být například Low vs. High (největší kontrast) a Lower-middle vs. Upper-middle (přechod přes nulu).

Kód z `Statistics_across_regions.ipynb` nelze přenést přímo — tam jsou skupiny regiony (Europe, Sub-Saharan Africa…), tady příjmové kategorie (Low income, Lower-middle income…). Logika testu je ale identická: `scipy.stats.mannwhitneyu(skupina_a, skupina_b)` — stačí přepsat filtry na sloupec `income_group`.

---

## Scatter plot Q1 — Pokud teda chcete dělat scatter plot v Pythonu a ne v PowerBI (ale stále tam tato část v repozitáři zůstává v Q1)

### Dva problémy v jedné buňce [`Q1-correlation_forest_GDP.ipynb`](scripts/statistics/Q1-correlation_forest_GDP.ipynb) - návod AI na opravu (samozřejmě)

**1. `plt.pyplot.xlabel` způsobí AttributeError — toto je reálná chyba, která zastaví spuštění buňky**

```python
plt.pyplot.xlabel('GDP per Capita')   # ← chyba — pyplot není atribut pyplot
plt.xlabel('GDP per Capita')           # ← správně
```

Import byl opravený na `import matplotlib.pyplot as plt` (dobrá oprava z minula), ale tohle místo zůstalo.

**2. Scatter plot zobrazuje lineární osu X, ale model byl nafitován v log-prostoru — vizualizace neodpovídá modelu**

```python
sns.regplot(x='gdp_per_capita', y='forest_change_pct', data=df_agregated, order=2)
```

`order=2` nafituje kvadratický (polynomiální) polynomiál v lineárním prostoru `gdp_per_capita` — ale váš OLS model pracoval s `np.log(gdp_per_capita)`. Výsledná křivka na grafu tedy zobrazuje jiný model, než ten který jste vypočítaly. Při prezentaci by EKC křivka měla odpovídat číslu $56 038 z výpočtu, ne jiné křivce z regplotu.

Pro správnou EKC vizualizaci použijte log(GDP) na ose X a nakreslete křivku přímo z modelu:

```python
df_agregated['log_gdp'] = np.log(df_agregated['gdp_per_capita'])

sns.scatterplot(x='log_gdp', y='forest_change_pct', data=df_agregated)

x_range = np.linspace(df_agregated['log_gdp'].min(), df_agregated['log_gdp'].max(), 200)
df_curve = pd.DataFrame({'np.log(gdp_per_capita)': x_range,
                          'np.power(np.log(gdp_per_capita), 2)': x_range**2})
y_curve = model_log.predict(df_curve)
plt.plot(x_range, y_curve, color='red', label='EKC model')

plt.xlabel('log(GDP per capita)')
plt.ylabel('Forest Cover Change (%)')
plt.axvline(turning_point, color='red', linestyle='--', label=f'Turning point (${tp_usd:,.0f})')
plt.legend()
plt.show()
```

---


## Logická nesrovnalost - definice „bohatý/chudý" v Q3 neodpovídá EKC v kontextu jiných částí projektu - není to nutně špatně, ale je potřeba se nad tím zamyslet a umět případně vysvětlit

### [`Q3-identifying_outliers.ipynb`](scripts/statistics/Q3-identifying_outliers.ipynb) — median GDP ≠ EKC turning point

Outlier skupiny jsou rozdělené takhle:

```python
poor_country_reforesting = df_agregated[
    (df_agregated['gdp_per_capita'] < median_gdp) &   # median = $4 828
    ...
]
rich_country_deforesting = df_agregated[
    (df_agregated['gdp_per_capita'] > median_gdp) &   # median = $4 828
    ...
]
```

Turning point z našeho vlastního Q1 modelu je **$56 038**. Příklad „bohatí odlesňovatelé":

| Země | Průměrné GDP | Turning point EKC |
|------|-------------|-------------------|
| Brazílie | $7 042 | $56 038 |
| Belize | $5 298 | $56 038 |
| Rovníková Guinea | $6 861 | $56 038 |

Tyto tři země jsou těsně nad mediánem, ale zároveň hluboko pod turning pointem. Z pohledu EKC se stále nacházejí na **levé straně křivky** — tzn. model pro ně odlesňování PŘEDPOVÍDÁ. To není paradox, to je očekávané chování.

#### Doporučuju buď:
- Explicitně napsat, že „bohatý/chudý" se v analýze definuje jako **nad/pod mediánem datasetu** (ne jako „bohatý v EKC smyslu"), nebo
- Přeformulovat závěr tak, aby nezněl, že tyhle země „překvapivě odlesňují přes svoje bohatství" — protože dle EKC to překvapivé není.

---

## Co dále odhalila AI při code review projektu:

### Vietnam — primární lesy klesají, přestože celkový pokryv roste [`Q3-outliers_closer_analysis.ipynb`](scripts/statistics/Q3-outliers_closer_analysis.ipynb) — tabulka 3 zůstane bez interpretace v Key Findings

**Kde to je v notebooku:** Tabulka 3 (`Naturally regenerating forest including primary forest`) je vytisknuta v sekci 3. Notebook má jedinou markdown buňku — úvodní Key Findings na začátku. Ta zmíní Vietnam jen v kontextu planted forests: *"Vietnam's planted forest exploded from near zero"*. Žádná jiná markdown buňka neexistuje, takže tabulka 3 zůstane bez interpretace.

**Co data říkají:**

| | 1990 | 2025 | Změna |
|--|------|------|-------|
| Naturally regenerating forest (1 000 ha) | 8 631 | 10 859 | **+26 %** |
| of which: Primary forest (1 000 ha) | **1 017** | **585** | **−42 %** |
| Planted forest (million m³ over bark) | 28,5 | 237 | **+733 %** |

Celkový lesní pokryv roste, ale struktura lesa se radikálně mění — primární prales ubývá a je nahrazován plantážemi.

**Proč na tom záleží:** Celý projekt stojí na metrice `forest_pct` — procentuálním podílu lesní plochy. Ta Vietnamu rostla a oprávněně ho zařadila mezi „chudé reforestery". Ale tabulka 3 ukazuje, že za tímto číslem se skrývají dva protichůdné trendy: mizící přirozené pralesy a masivní výsadba plantáží. Plantáže a primární les jsou z pohledu biodiverzity a uhlíkového skladu ekologicky zásadně odlišné — `forest_pct` je sečítá do jednoho čísla a jejich rozdíl tak není v datech vidět. Pokud tohle v závěru neuvedete, prezentace Vietnamu jako úspěšného příkladu zalesňování je technicky správná, ale nepřesná.

Stačí jedna věta navíc v Key Findings — například:

> *"Vietnam's overall forest cover grew (+26%), but primary forest declined by 42% — growth is driven by plantation expansion, not natural forest recovery."*

#### Názor můj:
Tohle by podle mě stálo za zmínku, protože je to jeden z halvních důvodů proč Q3 děláme, abychom zjistily tyto specifické vybočující případy a podívali se jim trochu více na zoubek

---

### Závěr o politice přesahuje to, co data ukazují [`Q3-outliers_closer_analysis.ipynb`](scripts/statistics/Q3-outliers_closer_analysis.ipynb) — sekce 5

#### Názor AI:
Key Findings říkají:

> *"Key differentiator is traceability and stakeholder participation — poor reforesting countries use centralized governance, rich deforesting ones have complex decentralized structures"*

Ale pohled na tabulku 5a+5b ukazuje, že vzor není tak čistý. Podívejte se na traceability a subnárodní governance pro obě skupiny vedle sebe:

- **Traceability**: VNM=yes, GHA=yes, BTN=yes, CUB=yes (reforestující) — ale BRA=yes, BLZ=yes (odlesňující). Traceability oba tábory oddělí jen napůl.
- **Subnárodní governance**: bez subnárodní mají VNM, RWA, CUB, BTN (reforestující) — ale taky BRN, GNQ (odlesňující). Se subnárodní mají BRA, ASM, BLZ (odlesňující) — ale taky Seychelly.

Data tedy ukazují smíšený vzor, ze kterého není možné udělat silný závěr o tom, co funguje a co ne. Závěr v Key Findings jde dál, než data dovolují.

Navrhuju formulovat opatrněji — zachovat pozorování, ale odebrat příčinné tvrzení:

> *"All 16 countries have national policies and legislation — policy existence alone does not differentiate the groups. Reforesting poor countries tend to operate through national-level governance only, while deforesting countries often have additional sub-national layers — though the causal link to forest outcomes is unclear from this data alone."*

#### Názor můj:
Předpokládám, že to nikdo kontrolovat nebude, takže si můžeme trochu přihřát polívčičku, jestli chceme a říct, že jsme to prokázali, ale byl bych opatrný s velmi razantními tvrzeními


---


### Chyba v jednotce — `forest_area_km2` obsahuje hektary, ne km² — [`03_fact_tables.ipynb`](scripts/database/03_fact_tables.ipynb)

Sloupec byl přidaný jako:

```sql
ALTER TABLE fact_forest ADD forest_area_km2 FLOAT;
```

Ale UPDATE ho počítá takhle:

```sql
SET forest_area_ha = (forest_pct / 100.0) * land_area_km2 * 100
```

Jméno sloupce je `km2`, vzorec dává **hektary** (`km² × 100 = ha`). Výsledek je vidět na světovém součtu z databáze — hodnota vychází přes **4 miliardy „km²"**, což je nesmysl: celková rozloha pevniny na Zemi je přibližně **149 milionů km²**. Hodnota je tedy o více než 25× větší než celá souš. Jako hektary to dává smysl — světová lesní plocha je přibližně 400–430 milionů ha, což číslu odpovídá.

Buď odeberte `* 100` ze vzorce (výsledek bude v km²), nebo přejmenujte sloupec na `forest_area_ha`. Záleží na tom, co potřebujete pro Power BI.

#### Názor můj:
Tohle bych opravil, je to chyba, která se jednoduše stane a ještě jednodušeji jde přehlédnout, ale bude dobré ji oddělat, kdyby se někdo koukal více do projektu


---

## Co se povedlo (podle AI, ale já vás chválím samozřejmě taky :)

**Q3-outliers_closer_analysis finální verze** — teď má 6 datových zdrojů a pokrývá celý outlier příběh od chráněných oblastí přes sázené lesy až po požáry. Intro markdown s Key Findings je dobrý nápad — čtenář ví, co hledat, než se dostane k tabulkám.

Závěr o Brazílii je výborný: *„enforcement gap, not policy gap"* — Brazílie má politiku, legislativu i traceability, ale 419 000 tis. ha požárů mluví za vše. To je přesná a dobře podložená formulace.

Cuba jako jediná země s **konzistentní přirozenou** obnovou (tabulka 2, natural expansion 38 tis. ha/rok v 90. letech) — tohle je zajímavý poznatek, který ostatní země nereplikují.

Income groups analýza — schodišťový vzor od −0.15 % (Low income) po +0.03 % (High income) s Kruskal-Wallis p ≈ 0 je přesvědčivý závěr a přirozeně navazuje na EKC hypotézu. Po doplnění pairwise testů bude analýza kompletní.

