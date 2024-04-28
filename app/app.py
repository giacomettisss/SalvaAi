from termcolor import colored
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already taken. Please choose a different one.', 'error')
            print(colored('Username already taken. Please choose a different one.', 'red', 'on_black'))
            return render_template('register.html')
        
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('User created successfully!', 'success')
            print(colored('User created successfully!', 'green', 'on_black'))
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Error creating user. Please try again.', 'error')
            print(colored('Error creating user. Please try again.', 'red', 'on_black'))
            return render_template('register.html')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            print(colored('Logged in successfully!', 'green', 'on_black'))
            return redirect(url_for('home'))
        else:
            flash('Invalid Credentials. Please try again.', 'error')
            print(colored('Invalid Credentials. Please try again.', 'red', 'on_black'))
            return render_template('login.html', error='Opa! errou!')
    return render_template('login.html')

@app.route('/')
def home():
    error = None
    print(colored('You are at home!', 'blue', 'on_black'))
    return render_template('mainv2.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)
