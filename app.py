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
    
def decrypt_password(encrypted_password):
    """
    Calls the C program to decrypt password
    """
    try:
        # Run the decrypt C program
        process = subprocess.Popen(
            ['decrypt.exe'],  # On Mac/Linux use './decrypt'
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Send encrypted password to C program
        output, error = process.communicate(input=encrypted_password.encode())
        
        # Get decrypted password
        decrypted = output.decode().strip()
        
        return decrypted
    except Exception as e:
        print(f"Decryption error: {e}")
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
    

    # Encrypt password using C program
    encrypted_password = encrypt_password(password)

    if encrypted_password is None:
        flash("Error encrypting password. Please try again.", "error")
        return redirect('/signup')

    # Save to file with ENCRYPTED password
    with open('users.txt', 'a') as f:
        f.write(f"{username},{email},{encrypted_password}\n")
    
    flash("Registration successful! Please log in.", "success")
    return redirect('/login')


# Login page route
@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('Email')
    password = request.form.get('Password')
    
    if not os.path.exists('users.txt'):
        flash("No users registered yet!", "error")
        return redirect('/login')
    
    user_found = False
    with open('users.txt', 'r') as f:
        for line in f:
            # Skip empty lines
            if not line.strip():
                continue
            
            # Split line and check if it has 3 parts
            parts = line.strip().split(',')
            
            # Add this check!
            if len(parts) != 3:
                print(f"Warning: Malformed line in users.txt: {line}")
                continue
            
            stored_username = parts[0]
            stored_email = parts[1]
            stored_encrypted_password = parts[2]
            
            if stored_email == email:
                user_found = True
                
                encrypted_entered_password = encrypt_password(password)
                
                if encrypted_entered_password == stored_encrypted_password:
                    flash(f"Welcome back, {stored_username}!", "success")
                    return redirect('/form')
                else:
                    flash("Incorrect password!", "error")
                    return redirect('/login')
    
    if not user_found:
        flash("Email not found. Please sign up first!", "error")
        return redirect('/login')
    
    return redirect('/login')

# Survey fourm page route
@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get all form data
    gender = request.form.get('gender')
    age = request.form.get('age')
    year = request.form.get('year')
    cgpa = request.form.get('cgpa')
    marital = request.form.get('marital')
    anxiety = request.form.get('anxiety')
    panic = request.form.get('panic')
    
    # Simple rule-based prediction (we'll replace with ML soon!)
    risk_score = 0
    
    age_num = int(age)
    if age_num < 20:
        risk_score += 15
    elif age_num < 25:
        risk_score += 10
    else:
        risk_score += 5
    
    year_num = int(year)
    if year_num >= 3:
        risk_score += 20
    else:
        risk_score += 10
    
    if cgpa == "2.50-2.99":
        risk_score += 25
    elif cgpa == "3.00-3.49":
        risk_score += 15
    else:
        risk_score += 5
    
    if anxiety == "Yes":
        risk_score += 30
    
    if panic == "Yes":
        risk_score += 10
    
    # Determine risk level
    if risk_score >= 70:
        risk_level = "High Risk"
        recommendation = "We strongly recommend speaking with a mental health professional."
        color = "high"
    elif risk_score >= 40:
        risk_level = "Moderate Risk"
        recommendation = "Consider talking to a counselor or trusted person about your feelings."
        color = "moderate"
    else:
        risk_level = "Low Risk"
        recommendation = "Keep maintaining healthy habits and reach out if you need support."
        color = "low"
    
    result = {
        'risk_score': risk_score,
        'risk_level': risk_level,
        'recommendation': recommendation,
        'color': color
    }
    
    # Render SAME PAGE with results
    return render_template('form.html', result=result)

@app.route('/admin')
def admin():
    # Read all users
    users = []
    
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                
                parts = line.strip().split(',')
                if len(parts) == 3:
                    users.append({
                        'username': parts[0],
                        'email': parts[1],
                        'encrypted_password': parts[2]
                    })
    
    return render_template('admin.html', users=users)

@app.route('/admin/reveal/<int:user_index>')
def reveal_password(user_index):
    # Read all users again
    users = []
    
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                
                parts = line.strip().split(',')
                if len(parts) == 3:
                    users.append({
                        'username': parts[0],
                        'email': parts[1],
                        'encrypted_password': parts[2]
                    })
    
    # Get the specific user
    if user_index < len(users):
        user = users[user_index]
        
        # Decrypt their password
        decrypted = decrypt_password(user['encrypted_password'])
        user['decrypted_password'] = decrypted
        
        return render_template('reveal.html', user=user)
    else:
        return "User not found", 404

@app.route('/test-decrypt')
def test_decrypt():
    encrypted = "Khoor123"
    decrypted = decrypt_password(encrypted)
    return f"Encrypted: {encrypted}<br>Decrypted: {decrypted}"

@app.route('/test')
def test():
    return "Backend is working! 🎉"

if __name__ == '__main__':
    app.run(debug=True, port=5000)