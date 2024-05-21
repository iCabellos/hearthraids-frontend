# hearthraids-frontend
- This project is about the idea of creating a unique TCG, leveraging algorithms and functions that are much more 
convenient on a computer while trying to stay as faithful as possible to a traditional TCG.


- Requirements
  - Python 3.10.11 (or higher)
  - Virtual env
  - Git

- Installation
  - Go to 'backend_hearthraid' root directory
  - ``` pip install -r requirements.txt ```

- Run API
  - Go to 'front-hearthraid' directory
  - Check migrations, first:
  - ``` python manage.py makemigrations ```
  - Then, migrate if have detected changes:
  - ``` python manage.py migrate ```
  - Run server, port 9000 for default
  - ``` python manage.py runserver 8000 ```
