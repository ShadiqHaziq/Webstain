from flask import Flask, redirect, url_for, session, request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os

app = Flask(__name__)
app.secret_key = "YOUR_SECRET_KEY"  # Replace with your secret key
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # For development only (http)

# Google OAuth 2.0 client configuration
client_secrets_file = "client_secret.json"  # Replace with the path to your client_secret.json

# OAuth 2.0 Flow setup
flow = Flow.from_client_secrets_file(
    client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://localhost:5000/callback"
)

@app.route('/')
def index():
    return '<button class="btnn"><a href="/login">Login with Google</a></button>'

@app.route('/login')
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)

    # Check the state
    if not session["state"] == request.args["state"]:
        return "State does not match!", 400

    credentials = flow.credentials
    service = build("oauth2", "v2", credentials=credentials)
    user_info = service.userinfo().get().execute()

    # Store user email in session
    session['email'] = user_info['email']
    return f'Logged in as: {session["email"]}'

if __name__ == "__main__":
    app.run(debug=True)
