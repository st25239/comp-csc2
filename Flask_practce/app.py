from flask import Flask, render_template, request, redirect, url_for, session, flash
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'


# Home page
@app.route('/')
def index():
    data = load_data()
    return render_template(
        'index.html',
        flowers=data['flowers'],
        addons=data['addons']
    )


# Add to cart page
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    return render_template("index1.html")


# Load JSON data
def load_data():
    with open('data/flowers.json') as file:
        flowers = json.load(file)

    with open('data/addons.json') as file:
        addons = json.load(file)

    return {
        'flowers': flowers,
        'addons': addons
    }


if __name__ == '__main__':
    app.run(debug=True)