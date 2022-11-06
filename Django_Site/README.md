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

#### Build/Run Locally ####

1. Build Docker container: ```docker build -t django_af_site .```
2. Run Docker container: ```docker run django_af_site``` (postgres should be running with dns of "db")
   

#### Upload to Registry ####

1. Build Docker container: ```docker build -t django_af_site .```
2. Create tag: ```docker tag django_af_site:latest <registry>/django_af_site:latest```
3. Upload to Docker Hub: ```docker push <registry>/django_af_site:latest```


### Further Information ###

1. [Docker with Django](https://docs.docker.com/samples/django/)