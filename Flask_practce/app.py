import datetime
import sqlite3

from flask import Flask, json, render_template, request, session, flash, redirect, url_for  
import json
app = Flask(__name__)
app.secret_key = 'your_secret_key'

def initalise_database():
    with sqlite3.connect ('flower_shop.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                cart TEXT NOT NULL,
                total REAL NOT NULL,
                invoice_number TEXT NOT NULL,
                invoice_date TEXT NOT NULL
            )
        ''')
        conn.commit()



@app.route('/calculate_total')
# Utility function to calculate total price of items in the cart
def calculate_total(cart, selected_addons):
    total = sum(details['quantity'] * details['price'] for details in cart.values())
    total += sum(price for price in selected_addons.values())
    return total
discount_applied = False
total = sum(details['quantity'] * details['price'] for details in cart.values())

if total > 100 and not discount_applied:
    discount = total * 0.10  # 10% discount
    total -= discount
    discount_applied = True


@app.route('/cancel_order', methods=['POST'])
def cancel_order():
    session.pop('cart', None)  # Clear the cart from the session
    session.pop('selected_addons', None)  # Clear the selected addons from the session
    flash('Order cancelled.')
    session.modified = True  # Force Flask to save the session
    return redirect(url_for('index'))  # Redirect to the index page after cancelling the order


@app.route('/')
def index(): 
    cart = session.get('cart', {})
    selected_addons = session.get('selected_addons', {}) # get selected addons from session
    flowers, addons = load_data()
    total = calculate_total(cart, selected_addons) # calculate total price
    return render_template ('index.html', flowers=flowers, addons=addons, cart=cart, total=total, selected_addons=selected_addons)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/checkout', methods=['POST'])
def checkout():
    customer_name = request.form['customer_name'].strip().title()
    cart = session.get('cart', {})
    selected_addons = session.get('selected_addons', {}) # get selected addons from session
    with sqlite3.connect('flower_shop.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO orders (invoice_number, customer_name, cart, total, addons, total) VALUES (?, ?, ?, ?, ?, ?)
        ''', (invoice_number, customer_name, json.dumps(cart), total, json.dumps(selected_addons), total))
        conn.commit()

        # make invoice file
        invoice_filename = f"{invoice_number}.txt"

        with open(invoice_filename, 'w') as f:
            f.write(f"Invoice Number: {invoice_number}\n")
            f.write(f"Customer Name: {customer_name}\n")
            f.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("Items:\n")
            for item, details in cart.items():
                f.write(f"{item}: {details['quantity']} X {details['price']} = ${details['quantity'] * details['price']:.2f}\n")
            if selected_addons:
                f.write("Add-ons:\n")
                for addon, price in selected_addons.items():
                    f.write(f"{addon} - Price: ${price:.2f}\n")

            f.write(f"Total: ${total:.2f}\n")
   

    if not customer_name:
        flash('Please enter your name before proceeding to checkout.')
        return redirect(url_for('index'))

    if not cart:
        flash('Your cart is empty. Please add items to your cart before checking out.')
        return redirect(url_for('index'))
    

    total = calculate_total(cart, selected_addons) # calculate total price
    invoice_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    invoice_number = f"INV-{customer_name.replace(' ', '_')}_{invoice_date}"

    with open('data/flowers.json', 'w') as f:
        f.write(invoice_number)

    return render_template('invoice.html', customer_name=customer_name, cart=cart, total=total, invoice_number=invoice_number, invoice_date=invoice_date, selected_addons=selected_addons)

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
    return redirect('/')

@app.route('/select_addon', methods=['POST'])
def select_addon():
    selected_addons = {}
    _, addons = load_data() # we only need addons 

    selected_keys = request.form.getlist('addons') # get list of selected addons from form

    for addon in selected_keys:
        if addon in addons:
            selected_addons[addon] = float(addons[addon]['price']) # store selected addon and its price

    session['selected_addons'] = selected_addons # store selected addons in session
    session.modified = True # force flask to save the session
    return redirect('/')# redirect to home or any other page where you want to display the selected addons





def load_data():
    with open('data/flowers.json') as file:
        flowers = json.load(file)
    with open('data/addons.json') as file:
        addons = json.load(file)  
 
    return flowers, addons






if __name__ == '__main__':
    initalise_database()
    app.run(debug=True)