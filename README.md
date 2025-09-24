## Live Website URL: [ahsoftware.club](ahsoftware.club)

## How to Run the Project Locally

1. Fork the website to your github account.
2. Use Pycharm to set up the code from your github fork.
3. Go to the terminal in PyCharm.
4. Run 
>pip install -r requirements.txt
5. Run __run.py__
6. Go to the link provided. http://127.0.0.1:5000/

## Index

1. Instance - Stores unreadable database file.
2. Migrations - Stores many different files used to configure/create SQLAlchemy database. Not to be changed regularly. 
3. Templates - Houses all HTML templates for each page that we serve to the user
4. Static
     - js - JavaScript files to be accessed by the HTML templates in the templates folder.
     - css - Houses CSS stylesheets to be accessed by the HTML templates in the templates folder.
5. Routes - Houses all URL extensions (i.e. /chatroom, /home, etc.)
     - auth - /login, /logout, and /register, as well as some logic for authenticating users
     - chatroom - /chatroom
     - monopoly - /monopoly
     - home - / and /home (same thing)
6. .gitignore - Use this file to make sure not to commit your cache information when contributing
7. app.py - Creates the flask application
     - **IMPORTANT**: if creating a new route or file, you **must** import the file in app.py **after** the original import block in the **second** import block. This prevents circular imports (**very bad things**)
8. config.py - Configures SQLAlchemy database
9. extensions.py - Sets up the socketIO object (client to server & vice versa communication)
10. forms.py - Stores templates for HTML forms as python code so that they can be properly authenticated (Mostly for login and registration purposes)
11. models.py - Classes to be stored in the database. If new objects need to be stored they should be added here.
12. properties.csv - A spreadsheet of all monopoly properties to be accessed when the game runs (which is not currently functional as of 09/24/25)
13. requirements.txt - A list of all required packages (see heading 2 in this README.md for usage)
14. run.py - See heading 2
15. wsgi.py - More socketIO configuration
