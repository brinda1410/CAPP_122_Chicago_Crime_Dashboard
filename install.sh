echo -e "1. Creating new virtual environment..."

python -m venv env 

echo -e "2. Installing Requirements..."

source env/Scripts/activate
pip install -r requirements.txt

deactivate 
echo -e "Install is complete."