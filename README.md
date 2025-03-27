##Household Service Application

It is a multi-user app (requires one admin and other service professionals/ customers) which acts as platform for providing comprehensive home servicing and solutions.


##AUTHOR
**Name**: Anisha Seth
**Email**: 23f1002056@ds.study.iitm.ac.in 

##DESCRIPTION:
The problem statement revolves around a multi-user app with admin(sole), customers and professionals taking on different responsibilities and functions in bringing this project together. The mandatory frameworks used were- Flask for application code, Jinja2 templates + Bootstrap for HTML generation and styling and SQLite for data storage. Herein, starting with a home page, we had make a login page for sign in of all users, two kinds of registration pages for customers and professionals respectively, three different kind of dashboards with home page, summary page, profile page and search functionality each based on the different users as well as implemented all the logic behind those functionalities. All in all, every user has a pivotal role bringing together a full circle to make this app work.
**Admin:** Creates, edits and deletes services, approves, rejects and deletes professionals and can also delete customers. Has access to all customers, professionals and service requests credentials. Is basically the soul of the app.      
**Customer:** Sends booking requests, closes accepted requests and gives feedback. Has access to all the services. Eyes of the app.
**Professional:** The foundation of the app, accepts or rejects service requests and provides customer rating.

##TECHNOLOGIES USED:

•	**Flask(Flask, render_template, request, url_for, redirect)** for application code
•	**Flask-SQLAlchemy:** ORM (Object-Relational Mapping) to handle database connections all  
                      around the app.
•	**HTML/CSS/JINJA2 TEMPLATES+BOOTSRTAP 5** for frontend user interface design. 
•	**OS** to interact with Operating System.
•	**Datetime** to time-stamping the python modules.
•	**Werkzeug** to work with uploaded files and check if they are secure.
•	**Matplotlib** to make interactive plots and for data visualization.
•	**SQLite:** A DBMS used for storing data.
