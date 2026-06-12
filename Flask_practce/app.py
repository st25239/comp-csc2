from flask import Flask, json, render_template, request, session, flash, redirect, url_for  
import json
app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/calculate_total')
# Utility function to calculate total price of items in the cart
def calclate_total(cart):
    total = sum(details['quantity'] * details['price'] for details in cart.values())
    return total

@app.route('/')
def index(): 
    cart = session.get('cart', {})
    flowers, addons = load_data()
    total = calclate_total(cart)
    return render_template ('index.html', flowers=flowers, addons=addons, cart=cart, total=total)

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

@app.route('/remove_from_cart/<item>')
def remove_from_cart(item):
    cart = session.get('cart', {})
     
    if item in cart:
        del cart[item]
        session['cart'] = cart
        session.modified = True
        flash(f'{item} removed from cart.')
    else:
        flash(f'{item} not found in cart.')

    return render_template('test.html')

@app.route('/select_addon', methods=['POST'])
def select_addon():
    selected_addon = {}
    _, addons = load_data() # we only need addons 

    selected_keys = request.form.getlist('addon') # get list of selected addons from form





def load_data():
    with open('data/flowers.json') as file:
        flowers = json.load(file)
    with open('data/addons.json') as file:
        addons = json.load(file)  
 
    return flowers, addons






if __name__ == '__main__':
    app.run(debug=True)