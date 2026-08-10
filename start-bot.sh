echo Checking for updates...
git pull
.venv/bin/pip install -r requirements.txt
echo Starting bot!
.venv/bin/python main.py | tee latest.log
echo Bot stopped
