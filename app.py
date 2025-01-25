from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
from forms import RegistrationForm, LoginForm
from models import register_user, get_user_by_email, init_mysql, get_game_logs
from config import Config
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

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
        return User(user[0], user[1])  # Assuming user[0] is the ID and user[1] is the username
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
    # Capture the 'next' parameter for redirection after login
    next_page = request.args.get('next')
    logging.debug(f"Next page parameter received: {next_page}")

    if form.validate_on_submit():
        # Get the user from the database
        user = get_user_by_email(form.email.data)

        if user:
            # Check if the password is correct
            if check_password_hash(user[3], form.password.data):
                # If login is successful, log the user in
                login_user(User(user[0], user[1]), remember=form.remember.data)  # Remember the user
                flash('Login successful!', 'success')

                # Redirect to the original destination (next) or dashboard
                if next_page:
                    logging.debug(f"Redirecting to next page: {next_page}")
                    return redirect(next_page)
                else:
                    logging.debug("No valid next page. Redirecting to dashboard.")
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
        game_logs = get_game_logs(current_user.id)  # Updated function call
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
    # Log unauthorized access attempts
    logging.debug("Unauthorized access detected.")
    
    # Capture the 'next' parameter if it exists, else fallback to the homepage
    next_page = request.args.get('next')
    logging.debug(f"Unauthorized redirect to login. Next page: {next_page}")

    # Redirect to the login page with next parameter (or default to home if none)
    return redirect(url_for('login', next=next_page))

if __name__ == '__main__':
    app.run(debug=True)
