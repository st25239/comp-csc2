import datetime
import sqlite3


from flask import Flask, app, json, redirect, redirect, render_template, request, session, flash, redirect, url_for
import json
app = Flask(__name__)
app.secret_key = 'I_love_my_mom'


















if __name__ == '__main__':
    initialise_database()
    app.run(debug=True)