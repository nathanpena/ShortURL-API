
# URL Shortener API with FastAPI and SQLite

This project is a **URL shortener** implemented using **FastAPI** and **SQLite** as the database. It provides endpoints to shorten URLs, redirect based on short URLs, track click counts, and reuse deleted URLs efficiently. The URL generator is optimized for low memory usage and ensures no duplicates by using a four-pointer system to introduce randomness and improve efficiency.

## Features

- Generate unique, short URLs from long URLs.
- Efficient URL reuse system using a pool of deleted URLs.
- Track the number of clicks each shortened URL receives.
- Optimized URL generation with low memory usage.
- Full API documentation available via FastAPI.

---

## Project Structure

```
.
├── generator.py          # Contains the logic for generating short URLs.
├── short_url_fastapi.py  # The main FastAPI application file with all the endpoints.
├── database.py           # Database configuration and setup using SQLAlchemy.
├── models.py             # Defines the database models for URL mappings and reuse pool.
```

---

## How It Works

1. **Short URL Generation**: 
   - The `generate_short_url` function generates URLs using a base-26 system (A-Z). The system keeps track of four pointers (`start`, `end`, `middle`, and `middle_plus_one`) to add randomness to the generated URLs.
   - This allows for efficient URL generation without consuming large amounts of memory and ensures there are no duplicates.
   
2. **Reuse Pool**: 
   - Deleted short URLs are added to a reuse pool. When generating a new short URL, the system first checks the pool for available URLs, ensuring efficient reuse of short URLs.
   
3. **Database Persistence**:
   - All URLs and click counts are stored in an SQLite database, ensuring data persists across server restarts.

---

## Prerequisites

- **Python 3.8+**
- **FastAPI** and **SQLAlchemy**
- **SQLite** (bundled with Python)

### Required Libraries:

Install the required dependencies using pip:

```bash
pip install fastapi uvicorn sqlalchemy
```

---

## Setting Up the Project

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/url-shortener.git
   cd url-shortener
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:

   You can run the FastAPI application with Uvicorn:

   ```bash
   uvicorn short_url_fastapi:app --reload
   ```

   This will start the application at `http://127.0.0.1:8000`.

---

## Interacting with the API

You can use **Postman** or **curl** to interact with the API.

### Base URL:

```
http://127.0.0.1:8000
```

### Endpoints:

1. **POST /shorten**

   **Description**: Shorten a new URL.

   - **Request**:
     - Method: `POST`
     - Body: `{ "url": "<original_url>" }`

   - **Example Request**:

     ```json
     {
       "url": "https://www.netflix.com"
     }
     ```

   - **Example Response**:

     ```json
     {
       "short_url": "AAAAA",
       "original_url": "https://www.netflix.com"
     }
     ```

   **Postman Example**:
   - **Method**: POST
   - **Body**: JSON `{ "url": "https://www.netflix.com" }`
   - **Response**: `{ "short_url": "AAAAA", "original_url": "https://www.netflix.com" }`

---

2. **GET /{short_url}**

   **Description**: Redirect to the original URL using the short URL.

   - **Request**:
     - Method: `GET`
     - URL: `/{short_url}`

   - **Example Request**:

     ```
     GET /AAAAA
     ```

   - **Example Response**:
   
     The response will redirect you to the original URL.

   **Postman Example**:
   - **Method**: GET
   - **URL**: `http://127.0.0.1:8000/AAAAA`

---

3. **GET /clicks/{short_url}**

   **Description**: Get the number of times a short URL has been accessed.

   - **Request**:
     - Method: `GET`
     - URL: `/clicks/{short_url}`

   - **Example Request**:

     ```
     GET /clicks/AAAAA
     ```

   - **Example Response**:

     ```json
     {
       "short_url": "AAAAA",
       "clicks": 1
     }
     ```

   **Postman Example**:
   - **Method**: GET
   - **URL**: `http://127.0.0.1:8000/clicks/AAAAA`

---

4. **DELETE /delete/{short_url}**

   **Description**: Delete a short URL and add it to the reuse pool.

   - **Request**:
     - Method: `DELETE`
     - URL: `/delete/{short_url}`

   - **Example Request**:

     ```
     DELETE /delete/AAAAA
     ```

   - **Example Response**:

     ```json
     {
       "message": "Short URL deleted and returned to the pool"
     }
     ```

   **Postman Example**:
   - **Method**: DELETE
   - **URL**: `http://127.0.0.1:8000/delete/AAAAA`

---

5. **GET /short_urls**

   **Description**: Retrieve all currently used short URLs.

   - **Request**:
     - Method: `GET`
     - URL: `/short_urls`

   - **Example Response**:

     ```json
     {
       "short_urls": ["AAAAA", "BBBBB"]
     }
     ```

   **Postman Example**:
   - **Method**: GET
   - **URL**: `http://127.0.0.1:8000/short_urls`

---

6. **GET /reuse_pool**

   **Description**: Retrieve all URLs in the reuse pool.

   - **Request**:
     - Method: `GET`
     - URL: `/reuse_pool`

   - **Example Response**:

     ```json
     {
       "reuse_pool": ["CCCC", "DDDD"]
     }
     ```

   **Postman Example**:
   - **Method**: GET
   - **URL**: `http://127.0.0.1:8000/reuse_pool`

---

## URL Generator Optimization

The short URL generator is optimized for low memory usage and avoids duplicates. Here's how it works:

1. **Base-26 Encoding**: The generator uses a base-26 system (A-Z) to create 5-character short URLs.
2. **Four-Pointer System**: To introduce randomness and avoid collisions:
   - Four pointers (`start`, `end`, `middle`, and `middle_plus_one`) are used to generate URLs from different parts of the range, ensuring uniform distribution.
3. **Efficient Memory Usage**: The generator doesn't store all possible combinations in memory but generates URLs dynamically as needed, ensuring optimal memory usage for large-scale operations.

---

## Running the Application

1. Clone the repository and navigate to the project directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the FastAPI server:
   ```bash
   uvicorn short_url_fastapi:app --reload
   ```
4. Access the API documentation:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

Feel free to contribute or raise issues in this repository!
