#--SCRIPT--
import os, kaggle, pandas as pd
from sqlalchemy import create_engine
# os      -> lets Python talk to file system (create folders, list files)
# kaggle  -> Kaggle's own library to download datasets
# pandas -> works with csv as a table
# create_engine -> helps Python connect to databases

# --- SETTINGS ---
KAGGLE_DATASET = "ashyou09/global-deforestation-and-afforestation-2000-2025"  #Kaggle url part which goes after www.kaggle.com/datasets/.You can change it for anything you want from Kaggle.
DOWNLOAD_DIR   = "/Users/beruska/Desktop/kaggle" # change the path to a folder where the CSV file will be saved.
TABLE_NAME     = "Forest_watch"               # name of the SQL table that you want to create

DB_HOST     = "db.czechitas.online"  # server address
DB_NAME     = "db_forestgdp"         # database
DB_USER     = "p_forestgdp"          # username to log in
DB_PASSWORD = "h0sPJ40jfN3$"         # password 

#1 DOWNLOADS THE FILE
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
# Creates the folder "....."
# exist_ok=True means: don't crash if the folder is already there

kaggle.api.dataset_download_files(KAGGLE_DATASET, path=DOWNLOAD_DIR, unzip=True)
# Downloads the dataset from Kaggle and saves it into the "....." folder in your PC

#2. READS THE FILE
df = pd.read_csv(os.path.join(DOWNLOAD_DIR, "global_deforestation_2000_2025.csv"))
#change the filename for what you have - check your DOWNLOAD_DIR folder after first run

#3. UPLOAD DATA TO DB
engine = create_engine(
    f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_HOST},3033/{DB_NAME}"
    f"?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
)
df.to_sql(TABLE_NAME, con=engine, if_exists="replace", index=False)
print("Done!")