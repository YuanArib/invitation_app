<h1>Web Based App</h1>
On going project created by Yuan Mizuna!#5858

<h2>How do I run this?</h2>

- First create python venv in the root directory (invitation_app), then activate it
    How to do it:
    - Create python env with `python -m venv {venv_name}
    - On Unix based OS (Linux and MacOS), activate it using the bash shell with: source /path/to/venv/bin/activate. (you usually need sudo)
    - On Windows, activate it using powershell with: ./path/to/venv/bin/Activate.ps1
- Install django with pip
- **Important: Run `python manage.py makemigrations` then `python manage.py migrate` to prepare all the django apps and models.**
- Run the development server with `python manage.py runserver`
- Go to 127.0.0.1:8000

<h2>urls map</h2>
- / = index
- /members = app_index
- /members/dashboard = dashboard
- /members/register = register

📓Notes:
Activate venv if you are going to do anything with django / python related in terminal (including running the server)
Open for Issues, will get this repo on private later.