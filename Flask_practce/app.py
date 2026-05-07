from flask import Flask, json, render_template, request, redirect, url_for, session, flash 

app = Flask(__name__)
app.secret_key = 'your_secret_key'



@app.route('/index')
def index():
    return render_template('index.html')    

def load_data():
    with open('data/flowers.json') as file:
        flowers = json.load(file)
        return flowers

if __name__ == '__main__':
    app.run(debug=True)