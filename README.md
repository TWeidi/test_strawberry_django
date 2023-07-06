Initialization
==============
Run the following commands to set up the virtual environment, populate the database and start the server:

```bash
poetry install
poetry shell
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata db.json
python manage.py runserver
```

Evaluate
========

Django REST
-----------
*   Go to http://127.0.0.1:8000/api-auth/components/.
*   Use the provided interface (<< Previous | Next >>) to retrieve new pages.
*   You can directly access the timing results from the Django Debug Toolbar on the left side.

Strawberry Django GraphQL
-------------------------
*   Go to http://127.0.0.1:8000/graphql/ for the GraphiQL interface.
*   Copy the query from <this_project_directory>/components/tests.py and paste it into the GraphiQL interface.
*   You can directly access the timing results from the Django Debug Toolbar on the left side.

Alternatively, you can run:
```bash
python manage.py test --keepdb
```
which is surprisingly faster by roughly a factor of 2 compared to the GraphiQL interface.

You can directly access the timing results from the Django Debug Toolbar on the left side.


Results
=======

*   REST endpoint: Approx. 500-700 milliseconds per 100 items page.
*   GraphiQL interface: Approx. 18 seconds for 100 items.
*   Direct GraphQL query of the schema via test: Approx. 7 seconds for 100 items.