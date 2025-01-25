import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
from forms import RegistrationForm, LoginForm
from config import Config

# Global variable to store the MySQL connection instance
db_connection = None

def init_mysql(app):
    """Initialize the MySQL connection with the Flask app."""
    global db_connection
    try:
        db_connection = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
        if db_connection.is_connected():
            print("MySQL Initialized successfully")
        else:
            print("Failed to initialize MySQL connection")
    except Error as e:
        print(f"Error: {e}")
        db_connection = None

def get_db_connection():
    """Check if MySQL is initialized and return the connection."""
    if db_connection is None or not db_connection.is_connected():
        raise ValueError("MySQL connection is not initialized or lost. Call init_mysql(app) first.")
    return db_connection

def register_user(username, email, password_hash):
    """Register a new user in the database."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
            (username, email, password_hash)
        )
        conn.commit()
        cur.close()
    except Error as e:
        if conn:
            conn.rollback()
        raise Exception(f"Error registering user: {e}")

def get_user_by_email(email):
    """Retrieve user details by email."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", [email])
        user = cur.fetchone()
        cur.close()
        return user
    except Error as e:
        raise Exception(f"Error fetching user: {e}")

def add_game_log(user_id, game_name, play_hours, play_date):
    """Add a new game log for a user."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO game_logs (user_id, game_name, play_hours, play_date) VALUES (%s, %s, %s, %s)", 
            (user_id, game_name, play_hours, play_date)
        )
        conn.commit()
        cur.close()
    except Error as e:
        if conn:
            conn.rollback()
        raise Exception(f"Error adding game log: {e}")

def get_game_logs(user_id):
    """Retrieve all game logs for a user."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM game_logs WHERE user_id = %s", [user_id])
        logs = cur.fetchall()
        cur.close()
        return logs
    except Error as e:
        raise Exception(f"Error fetching game logs: {e}")

def delete_game_log(log_id):
    """Delete a game log by ID."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM game_logs WHERE id = %s", [log_id])
        conn.commit()
        cur.close()
    except Error as e:
        if conn:
            conn.rollback()
        raise Exception(f"Error deleting game log: {e}")

# Initialize Flask app and configurations
app = Flask(__name__)
app.config.from_object(Config)

# Initialize MySQL connection
init_mysql(app)

# Initialize CSRF Protection
csrf = CSRFProtect(app)

# Flask-Login configuration
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirects to login if not logged in
login_manager.login_message_category = 'info'

# Flask session settings
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour session timeout

# User model
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    user = get_user_by_email(user_id)
    if user:
        return User(user[0], user[1])
    return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # Hash the password securely
            hashed_pw = generate_password_hash(form.password.data)

            # Register the user in the database
            register_user(form.username.data, form.email.data, hashed_pw)

            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Get the user from the database
        user = get_user_by_email(form.email.data)

        if user:
            # Check if the password is correct
            if check_password_hash(user[3], form.password.data):
                # If login is successful, log the user in
                login_user(User(user[0], user[1]), remember=form.remember.data)
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid password, please try again.', 'danger')
        else:
            flash('No account found with this email address.', 'danger')
        
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    # Fetch user-specific game logs or other data here
    try:
        game_logs = get_game_logs(current_user.id)  # Fetching game logs for logged-in user
    except Exception as e:
        game_logs = []
        flash(f"Error fetching game logs: {str(e)}", 'danger')

    return render_template('dashboard.html', username=current_user.username, game_logs=game_logs)

@app.route('/logout')
@login_required
def logout():
    logout_user()  # Logout the user
    flash('Logged out successfully', 'success')
    return redirect(url_for('home'))

# Custom error handler for unauthorized access
@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to access this page.', 'warning')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
