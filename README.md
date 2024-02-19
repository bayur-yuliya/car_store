1. Run docker
```
docker run -p 5432:5432 -e POSTGRES_PASSWORD=password postgres
```
2. Install dependencies
```
pip install -r requirements.txt
```
3. Models migrate
```
python manage.py migrate
```
4. Generate carshop data
```
python manage.py create_info
```
5. Generate cars
```
python manage.py cars
```
6. Run web server
```
python manage.py runserver
```