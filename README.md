Shopping Website Final Project

Project Overview

This project is a shopping website implemented using FastAPI, Streamlit, and several other tools and technologies. It includes a backend with database interactions, caching, and a user-friendly UI for managing the shopping experience.

Features

Backend: Developed using FastAPI for API management.

Database: MySQL is used to store data, initialized using Docker and managed via Beekeeper Studio.

Caching: Redis is integrated for caching to improve performance.

UI: Streamlit provides an interactive user interface.

Docker: Docker Compose is used to manage services and ensure easy setup.

Tech Stack

Programming Language: Python 3.11

Backend Framework: FastAPI

Frontend Framework: Streamlit

Database: MySQL

Caching: Redis

Containerization: Docker Compose

Database Management Tool: Beekeeper Studio

Prerequisites

Install Docker.

Install Beekeeper Studio.

Install Python 3.11 or later.

Install the required Python libraries by running:

pip install -r requirements.txt

Setup Instructions

Step 1: Clone the Repository

Clone this repository to your local machine:

git clone <repository_url>
cd shopping_website_final_project

Step 2: Start Services with Docker Compose

Start the database and Redis services using Docker Compose:

docker-compose up -d --build

This will start:

MySQL on port 3306

Redis on port 6379

Step 3: Initialize the Database

The database schema will be automatically initialized using the scripts in resources/db-migrations/ when the MySQL container starts.

Step 4: Run the Backend

Start the FastAPI backend server:

uvicorn main:app --reload

The API will be accessible at http://localhost:8000.

Step 5: Run the Streamlit UI

In a new terminal, start the Streamlit application:

streamlit run .streamlit/app/Home.py

The UI will be accessible at http://localhost:8501.

Usage

Use Beekeeper Studio to connect to the MySQL database at localhost:3306 with the credentials defined in docker-compose.yaml.

Interact with the backend API via FastAPI’s interactive docs at http://localhost:8000/docs.

Use the Streamlit UI to browse and interact with the shopping website.

File Structure

shopping_website_final_project/
├── .streamlit/                  # Streamlit configuration
├── config/                      # Configuration files
├── controller/                  # Controller logic
├── model/                       # Data models
├── redisClient/                 # Redis client configuration
├── repository/                  # Database repository layer
├── resources/db-migrations/     # Database initialization scripts
├── service/                     # Business logic layer
├── main.py                      # FastAPI entry point
├── docker-compose.yaml          # Docker Compose configuration
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation

Additional Notes

Caching: Redis is used for storing temporary data to enhance performance.

Database GUI: Beekeeper Studio provides an easy way to view and manage the MySQL database.

Streamlit: The UI allows you to interact with the backend seamlessly.

Commands Summary

Start Docker services:

docker-compose up -d --build

Start the FastAPI backend:

uvicorn main:app --reload

Start the Streamlit UI:

streamlit run .streamlit/app/Home.py

License

This project is licensed under the MIT License. See LICENSE for details.
