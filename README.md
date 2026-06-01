# World Forest Cover Change & GDP Correlation Analysis

> **Digital Academy Final Project** — A data analysis project exploring the relationship between global forest cover change and GDP per capita, tested against the Environmental Kuznets Curve (EKC) theory.
> 
> Final blog post published in Czech language on Medium (link below).

---

## Team
Kristina Kučerová
Barbara Kmeťová

---

## Research Focus

We focus on **world forest cover change per country** and its **correlation with GDP per capita**.

- **Forest data source:** FAO (FAOSTAT / Global Forest Resources Assessment) downloaded from Kaggle or FAO.
- **Forest definition:** Percentage of total land area covered with forest during a given year; excluding other wooded land — spanning more than 0.5 hectares, with trees higher than 5 meters and a canopy cover of 5–10%, or trees able to reach these thresholds in situ, or with a combined cover of shrubs, bushes and trees above 10%.
- **GDP data source:** World Bank via Kaggle (GDP per capita, current USD, 1960–2024)
- **Analysis period:** 1990–2025 (forest), 1990–2024 (GDP — 2025 not yet published by World Bank)
- **Countries covered:** ~214 countries with valid ISO3 codes

---

## Key Findings (updated 12/05/2026)

### Q1 — GDP & Forest Change Correlation (EKC)
| Metric | Result |
|--------|--------|
| Pearson r | 0.148 |
| P-value | 0.0 (significant) |
| R² | 0.148 — GDP explains ~14.8% of variance |
| EKC Turning Point | ~$56,038 GDP per capita |
| Quadratic term p-value | 0.051 — borderline, flagged |

- Weak but statistically significant positive correlation confirmed
- Inverted U-shape (EKC) confirmed - most countries are still on the upward slope
- Turning point corresponds to very wealthy nations (e.g. Austria, Netherlands, Sweden)

### Q1a — Income Groups
| Income Group | Avg. Annual Forest Change |
|---|---|
| Low income | -0.1499% |
| Lower middle income | -0.1054% |
| Upper middle income | -0.0044% |
| High income | +0.0335% |

- Kruskal-Wallis confirmed significant differences across all income groups (statistic: 929.94, p = 0.0)
- Clear staircase pattern — the richer the group, the better the forest trend

### Q2a — Regional Analysis
- Kruskal-Wallis confirmed significant regional differences (statistic: 2003.61, p = 0.0)
- Sub-Saharan Africa dominates the top 5 deforesters
- Europe is recovering — Montenegro, Serbia, Spain all in top 10 gainers
- Vietnam leads globally in reforestation
- Cuba is a surprising Latin American success story
- North America and South Asia show no significant difference despite very different economic levels

### Q3 — Outliers vs EKC Model
**Poor countries outperforming expectations (reforesting):**
- Vietnam: +17.28 pp (29.91% → 47.19%)
- Cuba: +12.63 pp (22.27% → 34.90%)
- Fiji: +10.78 pp (51.43% → 62.21%)
- Also: Jamaica, Rwanda, Ghana, Bhutan, Nepal, India, Burundi

**Rich countries underperforming (deforesting):**
- Seychelles: -16.55 pp (74.20% → 57.65%)
- Brazil: -15.83 pp (73.99% → 58.16%)
- Belize: -11.61 pp (69.26% → 57.65%)
- Also: American Samoa, Equatorial Guinea, Brunei Darussalam

> Note: "Rich/poor" here = above/below median GDP ($4,828), not the EKC turning point.

### Q4 — Population Density vs Forest Change
- Spearman r = 0.187, p = 0.0 → weak but significant **positive** correlation
- Opposite of the hypothesis — high-density countries are NOT the biggest deforesters
- Largest forest losses occur in low-to-medium density countries where land is abundant

---

## Repository Structure

```
digital_academy_project/
│
├── .gitignore
│
├── code/
│   ├── kaggle/
│   │   ├── Kaggle_instructions.py       # Setup guide: dependencies, Homebrew, ODBC driver
│   │   └── Kaggle_script.py             # Downloads dataset from Kaggle → uploads to SQL DB
│   │
│   ├── database/
│   │   ├── python_connect_db.ipynb              # DB connection template & usage examples
│   │   ├── 01_raw_data_exploration.ipynb        # Raw table inspection, quality checks, findings
│   │   ├── 02_dim-tables.ipynb                  # Builds dim_country and dim_year (dbo schema)
│   │   ├── 03_fact_tables.ipynb                 # Builds fact_forest and fact_gdp (dbo schema)
│   │   ├── Data_unpivot_from_raw_schema.ipynb   # Wide → long format transformation for Power BI
│   │   ├── Add_forest_change_pct_column.ipynb   # Calculates YoY forest change using Python diff()
│   │   └── Clean_GDP_country_names.ipynb        # Fixes CSV formatting issues in GDP source file
│   │
│   └── statistics/
│       ├── Q1-correlation_forest_GDP.ipynb          # Pearson correlation + EKC quadratic regression
│       ├── Q1a-income_groups.ipynb                  # Kruskal-Wallis + Mann-Whitney across income groups
│       ├── Q2a-regions.ipynb                        # Regional forest change analysis
│       ├── Q2b-subregions.ipynb                     # Subregional forest change analysis
│       ├── Q3-identifying_outliers.ipynb            # EKC residual-based outlier detection
│       ├── Q3a-outliers_closer_analysis.ipynb       # Deep dive into outlier countries
│       └── Q4-population_density_correlation.ipynb  # Spearman correlation: density vs forest change
│
└── powerBI/
    └── Final_report.pbix                   # Power BI dashboard — forest & GDP visualizations
```

---

## Database Schema

**Server:** `db.*********.online:****` | **Database:** `db_forestgdp`

### `raw` schema — source tables loaded as-is
| Table | Description |
|-------|-------------|
| `raw.Forest_year` | Forest coverage % per country per year (1990–2025) |
| `raw.GDP` | GDP per capita in USD per country (1960–2024) |
| `raw.Forest_Policy_Legislation` | National/sub-national forest policies |
| `raw.income_groups` | World Bank income group classifications |
| `raw.Land_Area` | Country land area in km² |
| `raw.Country_mapping` | ISO2/ISO3/region mapping |
| `raw.population_density_clean` | Population density per country per year |
| + 6 `_long` tables | Wide → long transformed FAO tables for Power BI |

### `dbo` schema — cleaned analytical tables
| Table | Description |
|-------|-------------|
| `dbo.dim_country` | Country dimension: code, name, region, subregion, income group, land area |
| `dbo.dim_year` | Year dimension (1990–2025) |
| `dbo.fact_forest` | Forest %, YoY change, area km², area weight per country/year |
| `dbo.fact_gdp` | GDP per capita per country/year |

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.14 | Data processing, statistics, DB connection |
| pandas | SQL Notebooks | Data manipulation |
| SQLAlchemy + pyodbc | Database connectivity |
| scipy | Statistical tests (Pearson, Spearman, Kruskal-Wallis, Mann-Whitney) |
| statsmodels | OLS regression (EKC quadratic model) |
| seaborn + matplotlib | Data visualisation |
| SQL Server (MS SQL) | Database (hosted on Czechitas server) |
| Kaggle API | Automated dataset download |
| Power BI | Dashboard & interactive visualisations |
| Jira | Project tracking |

---

## Setup & Installation (Mac)

### 1. Prerequisites
```bash
# Install Python libraries
pip3 install kaggle sqlalchemy pyodbc pandas scipy statsmodels seaborn matplotlib

# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install ODBC Driver 17 for SQL Server
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew install msodbcsql17
```

### 2. Kaggle API Setup
1. Go to [kaggle.com](https://www.kaggle.com) → Settings → API → **Create New Token**
2. Save the downloaded `kaggle.json` to your Desktop
3. Run:
```bash
mkdir -p ~/.kaggle && mv ~/Desktop/kaggle.json ~/.kaggle/ && chmod 600 ~/.kaggle/kaggle.json
```

### 3. Database Connection
Use `code/database/python_connect_db.ipynb` as a template. The connection string pattern:
```python
from sqlalchemy import create_engine, text
engine = create_engine(
    "mssql+pyodbc://<user>:<password>@db.czechitas.online,3033/db_forestgdp"
    "?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
)
```

### 4. Run Order (database notebooks)
```
01_raw_data_exploration → 02_dim-tables → 03_fact_tables
→ Data_unpivot_from_raw_schema → Add_forest_change_pct_column
```
Clean_GDP_country_names.ipynb is a one-time preprocessing step for the GDP source CSV.

---

## Project Status

| Task | Status |
|------|--------|
| Data sourcing & Kaggle pipeline | ✅ Done |
| Database schema (raw + dbo) | ✅ Done |
| Data cleaning & transformations | ✅ Done |
| Q1 — GDP correlation + EKC | ✅ Done |
| Q1a — Income groups | ✅ Done |
| Q2a — Regional analysis | ✅ Done |
| Q2b — Subregional analysis | ✅ Done |
| Q3 — Outlier identification | ✅ Done |
| Q3a — Outlier deep dive | ✅ Done |
| Q4 — Population density | ✅ Done |
| Q2 final comparison (GDP vs regions R²) | ✅ Done |
| Power BI dashboard | ✅ Done (v5) |
| Blog post (Czech) | ✅ Done (published on Medium) |

---

## Links

- [Jira Project Board](#) *(add link)*
- [Final Blog Post](https://medium.com/@beruska.jassova/vliv-ekonomického-rozvoje-států-na-plochu-lesů-964d17bf103b?postPublishedType=repub)

---

*Project developed as part of the Czechitas Digital Academy, 2026.*
