# FastAPI-User-Management-API

This is an API for managing users, implemented using FastAPI and SQLAlchemy.

## How to Run the Application

1. Clone this repository

    ```
    git clone https://github.com/zhengshunze/FastAPI-User-Management-API.git
    ```
    
2. Navigate to the project directory

    ```
    cd FastAPI-User-Management-API
    ```

4. Install the dependencies

    ```
    pip install -r requirements.txt
    ```
5. Run the application

    ```
    uvicorn main:app --reload
    ```


## How to Test API Endpoints


- **Create User**:
  -  POST /users/
  ```
  curl -X POST "http://127.0.0.1:8000/users/" -H "Content-Type: application/json" -d '{"name": "John Cena", "email": "john@example.com", "password": "wwechampion"}'
   ```

- **Get User**:
  -  GET /users/{user_id}
  ```
  curl -X GET "http://127.0.0.1:8000/users/1"
  ```
  
- **Update User**:
  - PUT /users/{user_id}
  ```
  curl -X PUT "http://127.0.0.1:8000/users/1" -H "Content-Type: application/json" -d '{"name": "ZXI-NA.ZHAO", "email": "ZXI-NA.ZHAO@example.com", "password": "championwwe"}'
  ``` 
- **Delete User**: 
  - DELETE /users/{user_id}
  ```
  curl -X DELETE "http://127.0.0.1:8000/users/1"
  ```
