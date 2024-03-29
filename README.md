# GitHub Parser

Data parser from GitHub

## Installation and Setup

1. Install Docker and Docker Compose if they are not already installed on your system.

2. Clone the project repository:

```bash
git clone https://github.com/Djama1GIT/github-parser.git
cd github-parser
```

3. Configure the environment variables in the .env-non-dev file

4. Start the project:

```bash
docker-compose up --build
```

## User Interface

After starting the project, you can access the Swagger user interface at: http://localhost:7354/docs.<br>
In Swagger, you can view the available endpoints and their parameters, and also make requests to the API.

## A few tests

**Note:** Install dependencies using ```pip install -r requirements.txt```.

```bash
pytest .
```

## Creating and invoking a cloud function
<h6>
It is assumed that you already have a postgresql server running. 
If this is not the case, you can uncomment the lines in docker-compose.yml and 
launch the container on Yandex Cloud.
</h6>

The function runs every half hour. 
I deemed it necessary to do so because it's not a very short or very long period, 
as there won't be too many changes during this time, and the number of API requests will be moderate.

```bash
/bin/bash ./src/github_parser/create_cloud_function.sh
```

Example:

![creating_function.png](creating_function.png)

![creating_function_2.png](creating_function_2.png)
