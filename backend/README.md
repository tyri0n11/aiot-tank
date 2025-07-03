# AI IoT Tank Backend

Flask-based backend for the AI IoT Tank project with MQTT support.

## Project Structure

```
backend/
├── app/
│   ├── __init__.py         # Flask app factory
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── user.py         # User management routes
│   │   ├── device.py       # Device management routes
│   │   └── mqtt.py         # MQTT routes
│   ├── models/
│   │   ├── user.py         # User model
│   │   └── device.py       # Device and SensorData models
│   ├── services/
│   │   ├── user_service.py    # User business logic
│   │   ├── device_service.py  # Device business logic
│   │   └── mqtt_service.py    # MQTT service
│   ├── extensions.py       # Flask extensions (db, bcrypt, jwt)
│   └── config.py           # Configuration
├── .env                    # Environment variables
├── requirements.txt        # Python dependencies
├── run.py                  # Application entry point
└── init_db.py             # Database initialization script
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Initialize the database:
```bash
python init_db.py
```

5. Run the application:
```bash
python run.py
```

## API Endpoints

### Health Check
- `GET /health` - Health check endpoint

### Users
- `GET /api/users/` - Get all users
- `GET /api/users/<id>` - Get user by ID
- `POST /api/users/` - Create new user
- `PUT /api/users/<id>` - Update user
- `DELETE /api/users/<id>` - Delete user

### Devices
- `GET /api/devices/` - Get all devices
- `GET /api/devices/<id>` - Get device by ID
- `POST /api/devices/` - Create new device
- `PUT /api/devices/<id>/status` - Update device status
- `DELETE /api/devices/<id>` - Delete device
- `POST /api/devices/<id>/sensor-data` - Add sensor data
- `GET /api/devices/<id>/sensor-data` - Get sensor data

### MQTT
- `POST /api/mqtt/publish` - Publish message to MQTT topic
- `POST /api/mqtt/subscribe/<topic>` - Subscribe to MQTT topic
- `GET /api/mqtt/status` - Get MQTT connection status

## Configuration

Key environment variables in `.env`:

- `SECRET_KEY` - Flask secret key
- `JWT_SECRET_KEY` - JWT secret key
- `DATABASE_URL` - Database connection string
- `MQTT_BROKER_HOST` - MQTT broker hostname
- `MQTT_BROKER_PORT` - MQTT broker port
- `MQTT_USERNAME` - MQTT username
- `MQTT_PASSWORD` - MQTT password

## Development

The application runs in debug mode by default. Access it at `http://localhost:8080`.

For production deployment, make sure to:
1. Set `FLASK_ENV=production`
2. Use a proper database (PostgreSQL, MySQL)
3. Configure proper MQTT broker credentials
4. Use a production WSGI server (Gunicorn, uWSGI)


## Test
