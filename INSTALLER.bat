cd PACKAGES

.\python-3.12.3-amd64.exe/passive AppendPath=1

cd ..\source
py -m venv .venv
call .venv\Scripts\activate


py -m pip install -r requirements.txt


py manage.py makemigrations
py manage.py migrate

