from flask import render_template
from flask_login import login_required
from app import create_app, db
from flask_migrate import Migrate
from flask_script import Manager

app = create_app()
migrate = Migrate(app, db)
# Create the database
db.create_all()

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/signup.html')
def signup():
    return render_template('signup.html')

@app.route('/dashboard.html')
@login_required
def dashboard():
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(debug=True, port=8080)
