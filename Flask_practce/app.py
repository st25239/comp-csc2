from flask import Flask, json, render_template, request, session, flash, redirect, url_for  
import json
app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/')
def index(): 
    flowers, addons = load_data()
    return render_template('index.html', flowers=flowers, addons=addons)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    flower = request.form.get('flower')
    quantity = int(request.form.get('quantity'))
    flowers, addons = load_data()
    cart = session.get('cart', {})

    if flower not in flowers:
        flash('Invalid flower selection.')
        return redirect(url_for('index'))
    
    if flower in cart:
        cart[flower]['quantity'] += quantity
    else:
        cart[flower] = {
            'quantity': quantity,
            'price': flowers[flower]['price']
        }

    session['cart'] = cart #update session
    session.modified = True # force flask to save the session
    flash(f'Added {quantity} {flower}(s) added to cart.')
    return redirect(url_for('index'))


def load_data():
    with open('data/flowers.json') as file:
        flowers = json.load(file)
    with open('data/addons.json') as file:
        addons = json.load(file)  
 
    return flowers, addons






if __name__ == '__main__':
    app.run(debug=True)