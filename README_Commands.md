# Check all the installed libraries
pip freeze
# Install djanga
uv pip install django
uv pip install djangorestframework
# to add django
uv add django
# to update the requirements.txt
uv pip freeze > requirements.txt
# to start a project 
django-admin startproject summarising_medical_test_api .
# to run the project
python manage.py runserver 1331
# to create a new app
python manage.py startapp medical_records
# to create migrations
python manage.py migrate
python manage.py createsuperuser
python manage.py makemigrations
# installing django filters
uv pip install django-filter
# React App creation
# use vite to create react app
npm create vite@latest
npm run dev
# You need node.js and npm to create an app and run an app in react.
# Installed Vite
# Installed ES7+ React/Redux/React-Native snippets by dsznajder
# Installed React developer tools as an extension
## React
Install react router dom 
# Handling CORS header
install django cors headers using the command pip install django-cors-headers

# Installing font awesome for react
follow the step on https://docs.fontawesome.com/web/use-with/react

# Installing djangorestframework sinplejwt

<!-- For production ready follow 
https://chatgpt.com/c/69e1ede4-8cc0-83eb-82d8-e84e28829e91
 -->