## Foodgram

Foodgram is a final study project of the Practicum 9-month backend developer course. I developed the backend from scratch and set up CI/CD.

The website allows users to publish recipes, subscribe to other users' publications, add favorite recipes to the "Favorites" list, and download a consolidated list of ingredients needed for selected dishes before going to the store.

## Stack

- Django
- Django Rest Framework
- PostgeSQL
- Docker
- Nginx
- Gunicorn

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
