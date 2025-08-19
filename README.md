# User Registration Website

[![Quality Gate Status](https://sonarqube-enterprise.demo.opsta.co.th/api/project_badges/measure?project=opsta_register-demo-app_36ebe093-bcc0-4164-8375-4ed6dd2a6aa3&metric=alert_status&token=sqb_f82d298d52dee00f7f12c91345a4e47d4369182b)](https://sonarqube-enterprise.demo.opsta.co.th/dashboard?id=opsta_register-demo-app_36ebe093-bcc0-4164-8375-4ed6dd2a6aa3)
[![AI Code Assurance](https://sonarqube-enterprise.demo.opsta.co.th/api/project_badges/ai_code_assurance?project=opsta_register-demo-app_36ebe093-bcc0-4164-8375-4ed6dd2a6aa3&token=sqb_f82d298d52dee00f7f12c91345a4e47d4369182b)](https://sonarqube-enterprise.demo.opsta.co.th/dashboard?id=opsta_register-demo-app_36ebe093-bcc0-4164-8375-4ed6dd2a6aa3)

A simple user registration website built with Flask, PostgreSQL, and Redis.

## Features

- User registration with email and name
- Email validation and uniqueness checking
- Redis caching for improved performance
- PostgreSQL database for persistent storage
- Modern, responsive UI
- Docker support for easy deployment

## Requirements

- Python 3.8+
- Docker and Docker Compose
- PostgreSQL 15
- Redis 7

## Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd register-demo-app
   ```

2. **Start the services**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Web app: http://localhost:5000
   - PostgreSQL: localhost:5432
   - Redis: localhost:6379

## Local Development Setup

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your local database credentials
   ```

3. **Start PostgreSQL and Redis**
   ```bash
   # Using Docker for services only
   docker-compose up postgres redis -d
   ```

4. **Run the Flask application**
   ```bash
   python app.py
   ```

## API Endpoints

- `GET /` - Homepage with registration form
- `POST /register` - Register a new user
- `GET /users` - Get all registered users
- `GET /health` - Health check for database and Redis connections

## Database Schema

```sql
CREATE TABLE users (
    email VARCHAR(120) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Redis Caching

The application uses Redis to cache user data temporarily before writing to the database:
- Cache key format: `user:{email}`
- TTL: 5 minutes
- Prevents duplicate registrations during high concurrency

## Project Structure

```
register-demo-app/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── docker-compose.yml # Docker services orchestration
├── templates/         # HTML templates
│   └── index.html    # Homepage template
├── env.example       # Environment variables template
└── README.md         # This file
```

## Environment Variables

- `FLASK_ENV`: Flask environment (development/production)
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_HOST`: Redis server hostname
- `REDIS_PORT`: Redis server port
- `SECRET_KEY`: Flask secret key for sessions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Run SonarQube

```bash
# The sonar token is mock up and can not be used
export SONAR_TOKEN=sqp_d6ae6bbe4b48ea29f573459462b90565e02dc123
pysonar \
  --sonar-host-url=https://sonarqube-enterprise.demo.opsta.co.th \
  --sonar-project-key=opsta_register-demo-app_36ebe093-bcc0-4164-8375-4ed6dd2a6aa3
```
