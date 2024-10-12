
git clone https://github.com/FujiwaraChoki/MoneyPrinterV2.git

# Copy Example Configuration and fill out values in config.json
cp config.example.json config.json

# Create a virtual environment
python -m venv venv

# Activate the virtual environment - Windows
.\venv\Scripts\activate

# Activate the virtual environment - Unix
source venv/bin/activate


pip install -r requirements.txt


python src/main.py