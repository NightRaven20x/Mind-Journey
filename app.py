from flask import Flask, render_template , request, jsonify , flash, redirect
import os

import subprocess

def encrypt_password(password):
    """
    Calls the C program to encrypt password
    """
    try:
        # Run the C program
        process = subprocess.Popen(
            ['encrypt.exe'],  # On Mac/Linux use './encrypt'
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Send password to C program
        output, error = process.communicate(input=password.encode())
        
        # Get encrypted password
        encrypted = output.decode().strip()
        
        return encrypted
    except Exception as e:
        print(f"Encryption error: {e}")
        return None

app = Flask(__name__)
app.secret_key = '12345' 

#password checker function
def check_password_strength(password):

    score = 0
    feedback = []

    #error of requirments 
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("✗ Too short (needs 8+ characters)")

    if any (c.isupper() for c in password):
        score += 1
    else:
        feedback.append("✗ Missing uppercase letters")
    
    if any (c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("✗ Missing numbers")

    special_chars = '#!@?'
    if any (c in special_chars for c in password):
        score += 1
    else:
        feedback.append("✗ Missing special characters (#!@?)")
    
    return score, feedback



# Home page route
@app.route('/')
def home():
    return render_template('home.html')

# Signup page - shows the form
@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    username = request.form.get('username')
    email = request.form.get('Email')
    password = request.form.get('Password')
    confirm_password = request.form.get('Confirm-Password')
    
    # Check if passwords match
    if password != confirm_password:
        flash("Passwords don't match! Please try again.", "error")
        return redirect('/signup')
    
    #strength checker function
    score , feedback = check_password_strength(password)

    if score < 2:
        return render_template('signup.html', 
                                password_error=True, 
                                feedback=feedback,
                                score=score,
                                username=username,
                                email=email)
    
    # Check if username already exists
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as f:
            for line in f:
                stored_username = line.split(',')[0]
                if stored_username == username:
                    flash(f"Username '{username}' already exists!", "error")
                    return redirect('/signup')
    
    # Save to users.txt (plain password for now)
    with open('users.txt', 'a') as f:
        f.write(f"{username},{email},{password}\n")
    
    flash("Registration successful! Please log in.", "success")
    return redirect('/login')


# Login page route
@app.route('/login')
def login():
    return render_template('login.html')

# Survey fourm page route
@app.route('/fourm')
def form():
    return render_template('fourm.html')

@app.route('/test')
def test():
    return "Backend is working! 🎉"

if __name__ == '__main__':
    app.run(debug=True, port=5000)