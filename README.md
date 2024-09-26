
git clone https://github.com/fxgurv/mp.git
cd mp
cp config.example.json config.json
python -m venv venv
.\venv\Scripts\activate
source venv/bin/activate
pip install -r requirements.txt
python src/main.py
