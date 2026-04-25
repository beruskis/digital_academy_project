import pandas as pd
cesta="/Users/kristyna/Desktop/CZECHITAS/Projekt/digital_academy_project/data_raw/Forest area compared to total area.csv"
df = pd.read_csv(cesta, header=[0, 1], index_col=0)
roky = ['1990', '2000', '2010', '2015', '2020', '2025']
vysledky = pd.DataFrame(index=df.index)
for rok in roky:
    les = pd.to_numeric(df[('Forest (1 000 ha)', rok)], errors='coerce')
    plocha = pd.to_numeric(df[('Total land area (1 000 ha)', rok)], errors='coerce')
    vysledky[rok] = les / plocha * 100
vysledky.to_csv('/Users/kristyna/Desktop/CZECHITAS/Projekt/digital_academy_project/scripts/Forest_area_percentage.csv')
