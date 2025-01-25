class Config:
    # MySQL Database configuration
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root2'
    MYSQL_DB = 'gaming_db'
    
    # Secret key for Flask sessions and CSRF protection
    SECRET_KEY = '8137bf29a364954c3aead4ba7156e9c645e860b7d1907cf203d53ec2df9878de'

    # Email server settings for sending notifications
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'shriharikasar1436@gmail.com'
    MAIL_PASSWORD = 'Shrihari@00096'

    # Optional: Set a default sender for email alerts
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
    
    # Session timeout (in seconds) for Flask
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour session timeout

    # Optional: Adjust logging level if needed (for debugging purposes)
    LOGGING_LEVEL = 'DEBUG'