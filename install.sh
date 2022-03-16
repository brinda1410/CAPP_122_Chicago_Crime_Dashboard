echo -e "1. Creating new virtual environment..."
python3 -m venv env 

echo -e "2. Installing Requirements..."

source env/bin/activate
pip install -r requirements.txt
python -m crimes_app

deactivate
rm -r env
echo -e "Bye bye! :D"