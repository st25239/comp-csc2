from flask import Flask, json, render_template, request, redirect, url_for, session, flash 
import json
app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')   
    return render_template('flowers.json')   
    return render_template('addons.json')    

@app.route('/Add to cart', methods=['POST'])
def add_to_cart():
    return render_template("index1.html")



@app.route('/index')
def index():
    flowers = load_data()
    return render_template('index.html', flowers=flowers)

def load_data():
    with open('data/flowers.json') as file:
        flowers = json.load(file)
        return flowers
    with open('data/addons.json') as file:
        addons = json.load(file)
    return {'flowers': flowers, 'addons': addons}

if __name__ == '__main__':
    app.run(debug=True)