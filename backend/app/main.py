# Entry point: creates the Flask app and registers each feature's Blueprint.
# Each routes/<feature>.py file defines a Blueprint named `bp` that holds that feature's routes.
from flask import Flask

from app.routes import feed, follows, rankings, restaurants, users

app = Flask(__name__)

app.register_blueprint(users.bp)
app.register_blueprint(restaurants.bp)
app.register_blueprint(rankings.bp)
app.register_blueprint(follows.bp)
app.register_blueprint(feed.bp)


# Health check: confirms the server is up without touching the database.
@app.route('/')
def main():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(debug=True, port=5001)
