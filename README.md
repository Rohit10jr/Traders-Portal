# Traders-Portal
fingrad job task

<!--  -->
python311 manage.py test
start htmlcov/index.html
coverage html 
coverage report
coverage run manage.py test
python311 manage.py shell < load_companies.py^C
netstat -ano | findstr :8000
taskkill /PID 3812 /F
celery -A traders_portal worker --loglevel=info --pool=solo
celery -A traders_portal beat --loglevel=info
redis-server.exe
find core/migrations -path "*__init__.py" -prune -o -name "*.py" -exec rm -f {} \;
find core/migrations -name "*.pyc" -delete
rm db.sqlite3

