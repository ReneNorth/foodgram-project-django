## Foodgram

Foodgram is a final study project of the Practicum 9-month backend developer course. I developed the backend from scratch and set up CI/CD.

The website allows users to publish recipes, subscribe to other users' publications, add favorite recipes to the "Favorites" list, and download a consolidated list of ingredients needed for selected dishes before going to the store.

### Tech stack

- React
- Django
- Django REST Framework
- PostgreSQL
- Docker
- nginx

### Installation

Clone the repository.
Rename dev.env to .env and change the constants to ones
you need to run the project.
Install Docker and Docker Compose.
Run the following command to build the project's Docker containers:

To run the project locally:

```console
cd infra/
docker-compose up --build -d
```

To launch the project on a VM

```console
cd infra/
docker-compose -r docker-compose.production up --build -d
```

A successful containers launch is followed by a similar output

```
[+] Running 5/5
 ⠿ Network infra_default       Created                                                 0.3s
 ⠿ Container infra-frontend-1  Started                                                12.7s
 ⠿ Container infra-db-1        Started                                                12.7s
 ⠿ Container infra-web-1       Started                                                20.4s
 ⠿ Container infra-nginx-1     Started
```

Once the containers are ready, enter the web container's CLI

```console
docker exec -it infra-web-1 bash
```

Run the following command to make migrations:

```console
python manage.py makemigrations
python manage.py migrate
```

Also, in case of running on a VM don't forget to change nginx settings

Run the following command to create a superuser and follow the prompts:

```console
python manage.py createsuperuser
```

then execute the commands to collect and move statics

```console
python manage.py collectstatic
cp -r /app/collected_static/. /backend_static/static/
```

Access the application at http://localhost:8000 or http://127.0.0.1:8000 or on your domain
Use the credentials of the superuser you created in the previous step to access django admin site /admin

### API docs

The docs are available at http://localhost:8000/api/redoc

## Features

Foodgram offers the following main features:

1.  **Homepage**: Displays a list of the six latest recipes sorted by publication date, with pagination for accessing more recipes.
2.  **Recipe Page**: Provides a detailed view of a recipe, including its description. Authenticated users can add the recipe to their favorites or shopping list and subscribe to the recipe's author.
3.  **User Profile Page**: Shows the user's name, all recipes published by the user, and an option to subscribe to the user.
4.  **Author Subscription**: Authenticated users can subscribe to authors by visiting their profile page or recipe page and clicking the "Subscribe to Author" button. The user can then view their subscribed authors' recipes on the "My Subscriptions" page, sorted by publication date.
5.  **Favorites List**: Authenticated users can add recipes to their favorites list by clicking the "Add to Favorites" button. They can view their personal list of favorite recipes on the "Favorites List" page.
6.  _(under development)_ **Shopping List**: Authenticated users can add recipes to their shopping list by clicking the "Add to Shopping List" button. They can access the "Shopping List" page, which provides a downloadable file containing a consolidated list of ingredients required for all the recipes saved in the shopping list.
7.  **Tag Filtering**: Clicking on a tag name displays a list of recipes tagged with that specific tag. Multiple tags can be selected to filter the recipes.
8.  **User Registration and Authentication**: The project includes a user management system, allowing users to register and authenticate themselves.

## For the Review

### domain https://foodgram.live/

### admin

admin login django: admin\
admin pass django: admin\
admin email: admin@admin.com

### user 1

username: Douglas_n\
email: Douglas_n@mail.com\
pass: Douglas_n@mail.com

### user 2

username: Rene_d\
email: Rene_d@mail.com\
pass: Rene_d@mail.com

### user 3

username: John_d\
email: anon@mail.com\
pass anon@mail.com
