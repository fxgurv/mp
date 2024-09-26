
git clone https://github.com/fxgurv/mp.git
cd mp
cp config.example.json config.json
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
python src/main.py
