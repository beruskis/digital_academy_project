#--INSTRUCTIONS!!!--
#download json file I saved on github as kaggle.json and save it on your DESKTOP!

#Instal in terminal before running the script below:
# 1. Install Python libraries
pip3 install kaggle sqlalchemy pyodbc

# 2. Install Homebrew (if not installed yet)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 3. Install ODBC Driver 17
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew install msodbcsql17

# 4. Create Kaggle folder (kaggle.json is on Desktop)
mkdir -p ~/.kaggle && mv ~/Desktop/kaggle.json ~/.kaggle/ && chmod 600 ~/.kaggle/kaggle.json