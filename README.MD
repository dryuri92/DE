<!-- ABOUT THE PROJECT -->
## About The Project

There is the simple backend project written as test task on python3 with FastAPI web-framework.

Application handles two endpoints:
* Get events from data store
* Post single event to data store

User can select one data store from two available options:
* PostgreSQL
* CSV formatted file `events.csv` from `./data` directory

<!-- GETTING STARTED -->
## Getting Started

The REST API specification is placed in this project repo `openapi_v1.0.1.yaml`.

### Prerequisites

To run localy you should have a >=python3.9 installed on your PC [https://www.python.org] (https://www.python.org)
To build and run application as a docker container you should install the docker following this guide [https://docs.docker.com/engine/install/] (docker-install)
It is recomended to use `make` to simplify installation process [https://www.gnu.org/software/make/] (make)

### Installation

0. Clone the repo with this project
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   cd ./Project-Name
   ```
1. The fastest way to run application is to use docker-compose
    ```sh
    make compose-postgres
    ``` 
   OR manually
    ```sh
    docker-compose -f .\compose\docker-compose.yaml up -d
    ``` 
    to run the light one version you can use *csv-file + pandas version:
    ```sh
    make compose-pandas
    ``` 
    alternative you can run the only application locally:
    ```sh
    make run-locally
    ```
2. To simply build docker image you can run:
   ```sh
   make build-docker
   ```
   or build/publish image to custom docker registry
   ```sh
   IMAGE_NAME:=<your_image> IMAGE_TAG := <your_tag> make publish
   ```

### Usage
The application can be customized using environmental variables:

| Variable Name | Description                              | Default    |
|---------------|------------------------------------------|------------|
| APP_HOST      | Application Host                         | 0.0.0.0    |
| APP_PORT      | REST API Port                            | 8888       |
| ENGINE        | Data Source: postgres/pandas             | postgres   |
| DBNAME        | Name of database: (only for postgres)    | test_db    |
| DBTABLE       | Name of table or path to  file with data | cd.events  |
| DBUSER        | User's name (only for postgres)          | root       |
| DBPASSWORD    | User's password (only for postgres)      | root       |
| DBPORT        | Database serving port(only for postgres) | 5432       |
| DBDATEFIELD   | Field name with datatime format          | event_date |

For example, app is available on your `localhost` and `:8888` port
You can send GET query using `curl`:
```sh
curl -X 'GET' \
  'http://localhost:8888/analytics/query?metrics=metric1&groupBy=attribute5%2Cattribute6&filters=attribute%3Aattribute6%2Cvalue%3Atrue&granularity=daily&startDate=2011-07-03T08%3A00%3A00' \
  -H 'accept: application/json'
```
or just copy-paste in your browser
`http://localhost:8888/analytics/query?metrics=metric1&groupBy=attribute5%2Cattribute6&filters=attribute%3Aattribute6%2Cvalue%3Atrue&granularity=daily&startDate=2011-07-03T08%3A00%3A00`

To add event to data store you should execute post-query:
```sh
curl -X 'POST' \
  'http://localhost:8888/event' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 201,
  "event_date": "2012-07-02T22:05:22",
  "attribute1": 2,
  "attribute2": 2,
  "attribute3": 3,
  "attribute4": "test-post",
  "attribute5": "12345",
  "attribute6": false,
  "metric1": 12,
  "metric2": 5.5
}'
```

<!-- LICENSE -->
## License

Distributed under the MIT License.

<!-- CONTACT -->
## Contact

Dr. Yuri

