from flask import Flask, json, render_template, request, session, flash, redirect, url_for  
import json
app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('test.html')   

if __name__ == '__main__':
    app.run(debug=True)







