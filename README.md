# Vehicle Parking Management System

A web-based parking management system built with Flask, SQLite, and Bootstrap.

## Features

- Multi-user system with Admin and User roles
- Parking lot management
- Real-time parking spot tracking
- User registration and authentication
- Booking and release of parking spots
- Dashboard with statistics and charts

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

5. Run the application:
```bash
flask run
```

The application will be available at http://localhost:5000

## Default Admin Credentials
- Username: admin
- Password: admin123

## License
MIT License 