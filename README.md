# Filter for pycantus
This project contains a Django template providing a web API for easily creating YAML files that help with the configuration of filtration in the [pycantus](https://github.com/dact-chant/PyCantus) library.  

It is deployed at [https://filterforpycantus.owx.cz](https://filterforpycantus.owx.cz).  
  
You can also easily plug this Django code into your app.

### How to use Filter for PyCantus as plugin in my Django web application

It is constructed as Django app, usage is similar to other extensions.

1. Run `pip install git+https://github.com/DvorakovaA/filterforpycantus.git` in the right environment where you develop your web application.

2. Add `filter` to INSTALLED_APPS in your web application
    ```
    INSTALLED_APPS = [
        ...
        "filter",
    ]
    ```

3. Run `python manage.py collectstatic`  
(make sure you have `django.contrib.staticfiles` in `INSTALLED_APPS` as well as `STATIC_ROOT` set in your `settings.py`)


4. Add filter urs into yours `urls.py`:  
    ```
    urlpatterns = [
        ...
        path("filter/", include("filter.urls")),
    ]
    ```

In case of troubles try to confront Django documentation about reusable apps installation.


### About project

Filter for pycantus (as well as PyCantus itself) is being developed under the Digital Analysis of Chant Transmission ([DACT](https://dact-chant.ca/)). This project, funded by the Social Sciences and Humanities Research Council of Canada, aims to advance the study of chant dissemination using computational tools.

Explore more about the project, its goals and contacts on our [homepage](https://ufal.mff.cuni.cz/grants/dact).