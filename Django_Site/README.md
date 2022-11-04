# Django AF Site # 

This is a Django project for the AF site for the cyber challenge. 

### Explanation ##

Here's the gist. 

- Two containers are created - Django and Postgres.
  
- The Django container will run the Django site in the AF directory. 
  - All settings are configured to attach to the postgres database by default 

- The Django container will make migrations, migrate, and the run the development server by default as pursuant by the entrypoint.sh file 

- There are two main pages - the homepage and the /admin directory. 

### Usage ###

To run the site: 
```docker compose up -d``` 

To stop the site: 
```docker compose down```

### Further Information ###

1. [Docker with Django](https://docs.docker.com/samples/django/)