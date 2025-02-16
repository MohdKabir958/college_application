from flask import Blueprint,render_template,request,redirect,flash,url_for
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth',__name__)

@auth.route('/profile')
def profile():
    return render_template('user_profile.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        name = fname + ' ' + lname
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        hashed_password = generate_password_hash(password=password, method='pbkdf2:sha256')
        
        if password != confirm_password: 
            flash("Passwords does'nt match")
            return render_template('signup.html', error='Passwords do not match')
        
        from . model import User
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("User with {} already exists! ".format(email))
            return render_template('signup.html')
        new_user = User(name=name, email=email, password=hashed_password)
        
        from .import db
        db.session.add(new_user)
        db.session.commit()
        flash('Signup successful! Please log in.')
        
        return redirect(url_for('auth.login'))

    return render_template('signup.html')
        



@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/logout')
def logout():
    return "Logout Successfull!"

