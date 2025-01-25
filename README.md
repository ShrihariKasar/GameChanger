# Flask Gaming App

A secure and user-friendly Flask-based gaming application with features like user authentication, session management, and game logs.

## Features

- User Registration and Login with secure password hashing.
- Session management with a 1-hour timeout.
- CSRF Protection for secure forms.
- Dynamic dashboard to view personalized game logs.
- Responsive design for a seamless user experience.

## Requirements

- Python 3.7+
- Flask
- Flask-Login
- Flask-WTF
- Werkzeug
- MySQL

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/flask-gaming-app.git
   cd flask-gaming-app
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your MySQL database and update the configuration in `config.py`.

5. Run the application:
   ```bash
   python app.py
   ```

6. Open your browser and navigate to `http://127.0.0.1:5000/`.

## Folder Structure

```
flask-gaming-app/
|-- templates/          # HTML templates
|-- static/             # CSS, JavaScript, and images
|-- app.py              # Main Flask application
|-- forms.py            # Form definitions (WTForms)
|-- models.py           # Database interaction logic
|-- config.py           # Application configuration
|-- requirements.txt    # Python dependencies
```

## Configuration

Update `config.py` with your database credentials and secret key:

```python
class Config:
    SECRET_KEY = 'your_secret_key'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'your_mysql_user'
    MYSQL_PASSWORD = 'your_mysql_password'
    MYSQL_DB = 'your_database_name'
```

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the [MIT License](LICENSE).