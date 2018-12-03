# Swagger generated server

## Overview
The skeleton for this server was generated by the [swagger-codegen](https://github.com/swagger-api/swagger-codegen) project. By using the
[OpenAPI-Spec](https://github.com/swagger-api/swagger-core/wiki) from a remote server, you can easily generate a server stub.

This example uses the [Connexion](https://github.com/zalando/connexion) library on top of Flask.
The generated server runs inside a docker container.

## Requirements
Python 3.6 +

## Usage
To run the server, please execute the following from the root directory:

```
docker-compose up --build
```

and open your browser to here:

```
http://0.0.0.0:8080/products-api/ui/
```

To launch the integration tests, use tox:
```
sudo pip install tox
tox
```

## Context

This service simulates an inventory management system for factories, where users are able to add products to an existing manufacturer's stock and list the current stock for that manufacturer.

It's possible to test these functionalities using the UI tool provided with this service. It's accessible via http://0.0.0.0:8080/products-api/ui/.

## Steps for development

I started by drawing the database structure's diagram in db_diagram.png . It needed to allow for enough abstraction that it is not dependent on the manufacturer's industry or the types of products that they store.

Next, I defined the contracts for the API and wrote its documentation in a swagger file using https://editor.swagger.io/. I then generated the server's skeleton using the same swagger file.
The generated server already handles the validation layer in a way that respects the contracts defined in the swagger file, and contains code stubs for the controllers. All I had to do was complete the controllers and define the database layer using Flask and SqlAlchemy (see 'db' folder).
the db_config.py script contains the database schema based on the database diagram.
The helpers.py script contain methods to read and save products to the database, and to convert a json payload to the database structure and vice-versa.

## How to test
In the swagger-ui browser interface, click 'Products' to expand the two existing endpoints, then click on the one you wish to test. the test/mocks folder contains two payload examples (the two files which name ends with 'post') can be used to create resources. The manufacturer is identified in the X_API_KEY box. Please note that only manufacturer names 'food' and 'textile' will work, others will trigger a 404 response. Also note the example column to the right to see how a valid payload looks like.

Note that the database is currently created from scratch every time the service is ran, and by default will only contain two default manufacturers.
