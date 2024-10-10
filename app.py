from flask import Flask, render_template, request

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return "Welcome to the Home Page"

# Login route to handle login form submission
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    # Simple authentication logic
    if email == 'test@example.com' and password == 'password123':
        return "Login successful!"
    else:
        return "Invalid credentials, please try again."

if __name__ == '__main__':
    app.run(debug=True)
