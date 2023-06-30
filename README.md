# API_Flask_Backend
A simple employee maintenance from multiple department using Python/Flask/PostgreSQL/Psycopg2
# Table Of Contents 
* Project overview
* Technologies used 
## Project overview 
Flask application that serves as an API for managing HR-related data stored in a PostgreSQL database. The application provides various endpoints for performing CRUD (Create, Read, Update, Delete) operations on employees and departments.

Here's a breakdown of the functionality provided by the API:

*GET /p.items: Retrieves a list of all employees along with their department and location details from the database.

*GET /p.item/<employee_id>: Retrieves a single employee's information based on the provided employee_id.

*DELETE /p.del-item/<d_department_id>/<employee_id>: Deletes an employee from the database based on the provided d_department_id and employee_id.

*POST /p.post-item: Adds a new employee and their corresponding department to the database. The employee and department details are provided in the request body.

*PUT /p.put-item/<d_department_id>/<employee_id>: Updates an existing employee's information in the database based on the provided d_department_id and employee_id. The updated , employee and department details are provided in the request body.

# Technologies used 
## Programming language 

* python - Python is a high-level, interpreted programming language known for its simplicity and readability. It is widely used for web development, data analysis, 
           scripting, and many other applications.
  
## Frameworks and libraries 

*Flask: Flask is a lightweight web framework for Python that is used to build the API endpoints and handle HTTP requests.

*psycopg2: Psycopg2 is a PostgreSQL adapter library for Python. It is used to establish a connection with the PostgreSQL database and execute SQL queries.

## Tools 
*Flask: Flask is a web framework for Python that allows you to build web applications and APIs. It provides routing, request handling, and other web-related functionalities.

*Psycopg2: Psycopg2 is a PostgreSQL adapter for Python. It allows Python applications to interact with PostgreSQL databases by providing a Python DB-API 2.0 compliant interface.

*PostgreSQL: PostgreSQL is an open-source relational database management system. It is used as the underlying database to store the HR-related data in this code.

*Git: Git is a distributed version control system. It is used for source code management, allowing you to track changes, collaborate with others, and manage different versions of your codebase.

*GitHub: GitHub is a web-based hosting service for Git repositories. It provides a platform for version control, collaboration, and hosting of your code repositories. It is commonly used for sharing and managing open-source projects.

*Postman or cURL: Postman and cURL are tools used for testing and interacting with APIs. They allow you to send HTTP requests to the API endpoints and examine the responses.
