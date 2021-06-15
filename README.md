# codus-w-django
A simple community website for programming language developed with Django.

## Demo
![Demo](https://github.com/chaebum-kim/codus-w-django/blob/master/demo.gif)

## Description
The goal of this project is to support simple CRUD and basic registration.<br>

1. Log in, Log out, Sign up
2. Upload/change profile image
3. Upload/edit/delete articles
4. Upload/edit/delete comments
5. Scrap an article
6. Support user page where you can
    - change your profile image
    - see the list of articles and comments you wrote
    - see the list of scrapped articles
7. Support github markdown(partially)
8. Support hashtags


## Installation
1. Clone this repository
```
git clone https://github.com/chaebum-kim/codus-w-django/
```
2. Download the requirements
```
python -m pip install -r requirements.txt
```
3. Make migrations
```
python manage.py makemigrations
```
```
python manage.py migrate
```
4. Run
```
python manage.py runserver
```


 
