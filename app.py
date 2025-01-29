from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

API_URL = "http://sse-lab10-book.dpckc9f4dcdpd6gw.westus2.azurecontainer.io:5000/"

def fetch_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, dict):  
            return data.get("books", [])
        elif isinstance(data, list):  
            return data
    return []

@app.route("/")
def home():
    return render_template("index.html")  # Homepage with form

@app.route("/submit", methods=["POST"])
def submit():
    genre_query = request.form.get("genre")  # Get user input from form
    books = fetch_data()

    # Filter books by genre if user entered a value
    if genre_query:
        genre_query = genre_query.lower()
        books = [book for book in books if genre_query in book.get("genre", "").lower()]

    return render_template("results.html", genre=genre_query, books=books)

if __name__ == "__main__":
    app.run(debug=True)
