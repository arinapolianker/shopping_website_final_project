# Shopping Website with ChatGPT Assistant

A full-stack e-commerce application built with FastAPI and Streamlit, featuring a ChatGPT-powered assistant for product inquiries.

## 🚀 Features

- **Product Management**: Browse, search, and filter products
- **Shopping Cart**: Add/remove items, manage quantities
- **Order System**: Create and manage orders
- **User Authentication**: Secure login and registration
- **ChatGPT Assistant**: AI-powered product assistance
- **Favorites System**: Save and manage favorite products

## 🛠 Tech Stack

### Backend
- Python FastAPI
- MySQL Database
- Redis Caching
- Docker Containerization

### Frontend
- Streamlit UI
- Python
- OpenAI ChatGPT API

### Testing & Development Tools
- Postman (API testing)
- Beekeeper Studio (database management)

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.9+
- OpenAI API Key
- Postman (for API testing)
- Beekeeper Studio (optional, for database management)

## 🔧 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd shopping_website_final_project
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   - Create a `.env` file in the root directory
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

4. **Start Docker containers**. Run these commands in sequence:
   ```bash
   # First, start the containers with the yaml configuration
    docker-compose -f docker-compose.yaml up
    
    # Then, rebuild and start in detached mode
    docker-compose up -d --build
   ```
   This will start:
   - MySQL database (port 3306)
   - Redis cache (port 6379)

## 🚀 Running the Application

1. **Start the FastAPI backend**
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://localhost:8000`

2. **Start the Streamlit frontend**
   ```bash
   streamlit run .streamlit/app/Home.py
   ```
   The web interface will open automatically at `http://localhost:8501`

## 📊 Database Management

You can view and manage the database using Beekeeper Studio:

1. Open Beekeeper Studio
2. Connect to MySQL with these credentials:
   - Host: localhost
   - Port: 3306
   - User: user
   - Password: password
   - Database: main

## 🤖 Using the ChatGPT Assistant

1. Navigate to the Chat Assistant page in the Streamlit UI
2. Enter your OpenAI API key in the sidebar
3. Start asking questions about products!

## 📁 Project Structure

```
shopping_website_final_project/
├── .streamlit/
│   └── app/
│       ├── pages/
│       └── Home.py
├── config/
│   └── config.py
├── controller/
├── exceptions/
├── model/
├── redisClient/
│   └── redis_client.py
├── repository/
├── resources/
│   └── db-migrations/
├── service/
├── docker-compose.yaml
├── main.py
├── README.md
└── requirements.txt
```

## 🔄 Development Workflow

1. Make changes to the code
2. If you modify the database schema:
   - Update the migration files in `resources/db-migrations`
   - Restart the Docker containers:
     ```bash
     docker-compose down
     docker-compose up -d
     ```

3. For frontend changes:
   - The Streamlit interface will automatically reload
   - Access the UI at `http://localhost:8501`

4. For backend changes:
   - The FastAPI server will automatically reload
   - Access the API docs at `http://localhost:8000/docs`

## 🛠 Troubleshooting

- **Database Connection Issues**
  ```bash
  docker-compose down
  docker volume rm shopping_website_final_project_mysql-data
  docker-compose up -d
  ```

- **Redis Cache Issues**
  ```bash
  docker-compose restart redis
  ```

- **Streamlit Port Already in Use**
  ```bash
  lsof -i :8501
  kill -9 <PID>
  ```

## 🔐 Security Notes

- Never commit your OpenAI API key
- Change default database credentials in production
- Use proper environment variables for sensitive data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Contact
Have questions? Feel free to reach out:
- **Email**: arinapolianker@gmail.com
- **LinkedIn**: [Arina Polianker](https://www.linkedin.com/in/arina-polianker-ab423b227/)
- **GitHub**: [arinapolianker](https://github.com/arinapolianker)



