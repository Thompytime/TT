import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for

# Load environment variables from .env file
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# Initialize Flask application
app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

# Configure OAuth with Auth0
oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)

# Routes

@app.route("/")
def home():
    return render_template(
        "home.html",
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )

@app.route('/MensEuro2024')
def mens_euro_2024():
    return render_template('MensEuro2024.html')

@app.route('/womens_euro_2025')
def womens_euro_2025():
    return render_template('WomensEuro2025.html')

@app.route('/mens_world_cup_2026')
def mens_world_cup_2026():
    return render_template('MensWorldCup2026.html')

@app.route('/womens_world_cup_2027')
def womens_world_cup_2027():
    return render_template('WomensWorldCup2027.html')

@app.route('/MensEuro2024a')
def mens_euro_2024a():
    return render_template('TC1.html')

@app.route('/womens_euro_2025a')
def womens_euro_2025a():
    return render_template('TC2.html')

@app.route('/mens_world_cup_2026a')
def mens_world_cup_2026a():
    return render_template('TC3.html')

@app.route('/womens_world_cup_2027a')
def womens_world_cup_2027a():
    return render_template('TC4.html')

@app.route('/MensEuro2024b')
def mens_euro_2024b():
    return render_template('TS1.html')

@app.route('/womens_euro_2025b')
def womens_euro_2025b():
    return render_template('TS2.html')

@app.route('/mens_world_cup_2026b')
def mens_world_cup_2026b():
    return render_template('TS3.html')

@app.route('/womens_world_cup_2027b')
def womens_world_cup_2027b():
    return render_template('TS4.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

# Authentication routes

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/logout")
def logout():
    session.clear()
    return_to = url_for("home", _external=True)  # Redirect back to home after logout
    logout_url = (
        "https://" + env.get("AUTH0_DOMAIN") + "/v2/logout"
        + "?returnTo=" + quote_plus(return_to)
        + "&client_id=" + env.get("AUTH0_CLIENT_ID")
    )
    return redirect(logout_url)

# Run the application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3000))
