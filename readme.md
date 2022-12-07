# Trading System

Trading System APIs using Python (Django)
1.  [APIs Documentation](https://documenter.getpostman.com/view/12162243/2s8YzP35YL)

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
    docker exec -it trading-system_app_1 python manage.py migrate

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
docker-compose.yml
manage.py
readme.md
config
   |-- __init__.py
   |-- asgi.py
   |-- mqtt_client.py
   |-- settings.py
   |-- urls.py
   |-- wsgi.py
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

You can also find the postman collection from [here](https://documenter.getpostman.com/view/12162243/2s8YzP35YL)

```
Method  URI Pattern
----  -----------
GET   api/users/
POST  api/users/
GET   api/users/<user_id>/
POST  api/users/<user_id>/deposit/
POST  api/users/<user_id>/withdraw/
POST  api/users/<user_id>/buy/
POST  api/users/<user_id>/sell/
GET   api/stocks/
GET   api/stocks/<stock_id>/
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

you could find the others APIs in the postman collection


## 🗒  Appendix
In this project I used django (python) to consume ``VerneMQ`` topic, I used ``Phao`` client to connect to this topic and consume it. Each message I receive from the topic I insert it to ``postgresSQL `` database.

##### In MQTT Client
I used phao client to consume the topic and in the client i opend non-blocking connection so i can run it in my project without blocking the others requests, I tried to run the client in differnt places ( when init the project, configure the apps inside the project) but it seems like its not the best place so i added it in the wsgi files and its working perfectly. 

##### In buy/sell 
when the user create ``buy/sell`` order if the user has the total money ( total * upper bound) that he wrote in the upper bound the the system will freeze this amount and add this order to pending orders table and check in every message i receive if i there are any match with any of the pending orders i complete the transactions and remove the order from pending orders. The order could be done in multiable transactions E.g:

> if I created buy order with ``` upper_bound:20,total:100 ``` and the
> current stock price is ```price:20, avalablity:50 ```  the user will
> get the 50 stock and when it match again with the price in another
> message the user will take the rest of the total

also i have ``Userstocks``  and ``userTransactions`` table, userStocks unique within user_id and stock_id to save only the total of each stock. In the userTransactions i save all the transactions with the price of each buy/sell transaction so i can track all the prices.

To handle any ``race condition`` or any ``duplicate  ``  I created atomic transaction with locking in the insertions of the order so I can make sure there are no duplicates 





