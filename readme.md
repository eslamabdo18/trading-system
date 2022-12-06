# Trading System

Trading System APIs using Python (Django)

## 🧑🏽‍💻 Technologies used

Project created with :

1. **Django:** I used ruby to create the main core management functionality.
2. **PostgresSQL:** The main database
3. **Phao:** client to handle the mqtt topic from python
4. All the testing tools like `Coverage` `FactoryBot` `Faker`

## ⚡️ Quick start

> Make sure that `docker` and `docker-compose` are installed with `docker` running.

    git clone https://github.com/eslamabdo18/trading-system
    cd trading-system
    docker-compose up -d --build

> This may take sometime to run the project

and to run the test cases

    docker exec -it trading-system_app_1 coverage run manage.py test -v 2

if you want to access the admin page to see all the database models ,first you have to create superuser account. After creating the superuser account please click [here](http://localhost:8000/admin)

```
docker exec -it trading-system_app_1 python manage.py createsuperuser
```

> the docker should be running so you can open the admin page

## ✍🏼 Project Structure

In this project i created three separates apps one for all the user operations (get user, sell, buy, deposit) and the second for all the stocks operations and the last one is only a order engine matcher to handle the match mechanism of buy or sell

```
Dockerfile
Pipfile
Pipfile.lock
config
   |-- __init__.py
   |-- asgi.py
   |-- mqtt_client.py
   |-- settings.py
   |-- urls.py
   |-- wsgi.py
docker-compose.yml
manage.py
readme.md
stocks
   |-- __init__.py
   |-- admin.py
   |-- apps.py
   |-- migrations
   |-- models.py
   |-- mqtt.py
   |-- serializers.py
   |-- services.py
   |-- tests.py
   |-- urls.py
   |-- views.py
trade
   |-- order_matcher.py
   |-- trade_service.py
users
   |-- __init__.py
   |-- admin.py
   |-- apps.py
   |-- migrations
   |-- models.py
   |-- serializers.py
   |-- tests
   |   |-- __init__.py
   |   |-- test_models.py
   |   |-- test_views.py
   |-- urls.py
   |-- views.py
```

## 👀 APIs Routes

You can also find the postman collection from [here](https://documenter.getpostman.com/view/12162243/2s8YYEPQvR)

```
Method  URI Pattern
----  -----------
GET   api/users/
POST  api/users/
GET   api/users/<user_id>
POST  api/users/<user_id>/deposit
POST  api/users/<user_id>/withdraw
POST  api/users/<user_id>/buy
POST  api/users/<user_id>/sell
GET   api/stocks
GET   api/stocks/<stock_id>
```

## 💡 How to use

**Get user**

```
# using cURL
curl -X GET http://localhost:8000/api/users/1/

# using httpPie
http GET :8000/api/users/1/
```

> output:

```
{
    "username": "eslam",
    "email": "es@gmail.com",
    "balance": 19402.0,
    "stocks": [
        {
            "stock_id": "cf12d54e-58ee-4a98-b56f-929ab222db3e",
            "name": "Edita",
            "total_count": 360
        },
        {
            "stock_id": "68d567d4-3661-4793-97a3-f75145987056",
            "name": "Hamada Inc",
            "total_count": 380
        },
        {
            "stock_id": "c5165fef-bb13-4913-b92a-0eef45b3d53e",
            "name": "CIB",
            "total_count": 100
        }
    ],
    "recent_transactions": [
        {
            "stock": "Edita",
            "type": "Buy",
            "stock_price": 5.0,
            "total_price": 500.0,
            "total_count": 100
        },
        {
            "stock": "Edita",
            "type": "Buy",
            "stock_price": 7.0,
            "total_price": 700.0,
            "total_count": 100
        },
        {
            "stock": "Edita",
            "type": "Buy",
            "stock_price": 6.0,
            "total_price": 114.0,
            "total_count": 19
        },
        {
            "stock": "Edita",
            "type": "Buy",
            "stock_price": 6.0,
            "total_price": 114.0,
            "total_count": 19
        },
        {
            "stock": "Edita",
            "type": "Buy",
            "stock_price": 27.0,
            "total_price": 1539.0,
            "total_count": 57
        }
    ]
}
```

**get stock**

```
# using cURL
curl -X GET http://localhost:8080/api/stocks/c5165fef-bb13-4913-b92a-0eef45b3d53e/

# using httpPie
http GET :8080/api/stocks/c5165fef-bb13-4913-b92a-0eef45b3d53e/
```

> output:

```
{
    "stock_id": "c5165fef-bb13-4913-b92a-0eef45b3d53e",
    "name": "CIB",
    "highest_price": 417.0,
    "lowest_price": 0.0,
    "average_price": 79.54771610118691,
    "recent_data": [ #get every time the recent 5 streams
        {
            "price": 186.0,
            "availability": 33,
            "timestamp": "2022-12-03T18:01:28.745401Z"
        },
        {
            "price": 32.0,
            "availability": 48,
            "timestamp": "2022-12-03T18:01:29.154429Z"
        },
        {
            "price": 32.0,
            "availability": 48,
            "timestamp": "2022-12-03T18:01:29.154429Z"
        },
        {
            "price": 93.0,
            "availability": 139,
            "timestamp": "2022-12-03T18:01:29.743429Z"
        },
        {
            "price": 33.0,
            "availability": 201,
            "timestamp": "2022-12-03T18:01:30.425108Z"
        }
    ],
    "transactions": [
        {
            "user": "eslam",
            "type": "Buy",
            "stock_price": 28.0,
            "total_price": 560.0,
            "total_count": 20
        },
        {
            "user": "eslam",
            "type": "Sell",
            "stock_price": 28.0,
            "total_price": 560.0,
            "total_count": 20
        },
        {
            "user": "eslam",
            "type": "Buy",
            "stock_price": 16.0,
            "total_price": 1296.0,
            "total_count": 81
        },
        {
            "user": "eslam",
            "type": "Buy",
            "stock_price": 18.0,
            "total_price": 342.0,
            "total_count": 19
        }
    ]
}
```

we could also get stock data within a datetime range and in this case we specify the url as the example below

    http://localhost:8000/api/stocks/c5165fef-bb13-4913-b92a-0eef45b3d53e?from_date=2022-12-05 00:00:00&to_date=2022-12-06 00:00:00

> we could filter by any range of dates or by any time in a specific date if i want to get the data in hour from_date will be 2022-12-05 04:00:00 and to_date will be 2022-12-05 05:00:00. if you want to get data between 2 dates without time you have also to specify the time frame to 00:00:00 as mentioned in the url above
