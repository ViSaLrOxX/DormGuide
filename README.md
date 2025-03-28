# DormGuide
Web Application Design 2nd year University of Glasgow Project

Setting up virtual enviroment:-
python -m venv venv

#Activate environment 
source venv/bin/activate      # for Linux/Mac
.\venv\Scripts\activate         #for Windows

#Install Dependencies
pip install django
pip install psycopg2
pip install django-registration
pip install django-allauth
pip install django-bootstrap5
pip install django-leaflet
pip install gdal
pip install geos
pip install django-crispy-forms

#Start Server
python manage.py runserver
