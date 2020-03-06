This project was designed and implemented by Nouran Alotaibi and Michael Katz.

vvv *** IMPORTANT *** vvv

Before reading this file or attempting to run the app, some things need to be installed using a pip install.

- pip install flask
- pip install flask-sqlalchemy
- pip install flask-wtf
- pip install flask-login
- pip install flask-bcrypt

^^^ *** IMPORTANT *** ^^^


The project is separated into distinct sections that this file will provide a rough overview for. More detail regarding
a specific file can be found in each respective file.

1. run.py
    - This is the file that when ran, calls on the Flask app from the __init__.py file.

2. __init__.py
    - This file initiates many of the essential parts of the program.
    - 1. Initiates the Flask app.
    - 2. Initiates the sqlite3 database.
    - 3. Initiates login manager.
    - 4. Initiates the Bcrypt encryption extension for password encryption.

3. routes.py
    - routes.py provides most of the functionality that is seen within the website. This file basically lays out
      the guidelines for every page or interaction that occurs on the website. Details pertaining to each route can
      be found within the docstring for that route in the routes.py file. All routes server one of three main
      functionalities: GET, POST, and GET/POST. The GET routes bring information from the database to the webpage. The
      POST routes take information from the webpage and add them to the database. The GET/POST routes can do either.

4. forms.py
    - forms.py uses the useful Flask extension called Flask-WTF, which is an extension itself of WTForms. This extension
      allows web forms to be made easily and quickly. These forms allow the user to input information into the website
      as well as retrieve it (depending on the route). The information inputted into these forms eventually gets used
      in the routes.py file.

5. filldatabase.py
    - This file does exactly what the name describes, it resets and refills the database with new and random entries.

6. models.py
    - models.py provides the database with the framework for every table that gets inserted into it. As I believe
      SQLAlchemy to work, when the program is ran it also checks to make sure if what is in the database matches up with
      how the models are currently setup. So if a change is made to the models without resetting and refilling the
      database, then I believe and error will be thrown.

7. storedProcedures.py
    -

8. testFunctions.py
    -