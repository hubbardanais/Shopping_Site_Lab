"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken, Katie Byers.
"""

from flask import Flask, render_template, redirect, flash, session, request
import jinja2

import melons

app = Flask(__name__)

# A secret key is needed to use Flask sessioning features
app.secret_key = 'bjWIUAHDiedkjaKLjdo;HDdKADHAILWDhAODW;j8932'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.
app.jinja_env.undefined = jinja2.StrictUndefined

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    print(melon)
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Melon successfully added to
    cart'."""

    if "cart" not in session:
        session['cart'] = {}

    if melon_id in session['cart']:
        session['cart'][melon_id] += 1
    else:
        session['cart'][melon_id] = 1

    session.modified = True

    flash('Melon successfully added to your cart!')

    return redirect('/cart')


@app.route("/cart")
def show_shopping_cart():
    """Display content of shopping cart."""

    cart_subtotal = 0
    cart_melons = []

    # The logic here will be something like:
    
    if "cart" not in session:
        session['cart'] = {}
  
    cart = session.get("cart")

    """

    request.args -> used to gather information sent in an html form as a get request. request.args is a dictionary

    request.forms -> used to gather information sent in an html form as a POST request. request.forms is a dictionary
    
    """

    # - create a list to hold melon objects and a variable to hold the total
    #   cost of the order @@@
    """
    cart = {
    'jubli' : 5,
    'sugby' : 2,
    'irish' : 2
    }
    jubli - $5 - -- $25
    sugby - $3   -- $6
    irish - $4   -- $8

    total = 38
    """
    # - loop over the cart dictionary, and for each melon id:
    for melon_id in cart.keys():
    #    - get the corresponding Melon object
        melon = melons.get_by_id(melon_id)
    #    - compute the total cost for that type of melon
        
    #    - add this to the order total
        cart_subtotal += melon.price * session['cart'][melon_id]
    #    - add quantity and total cost as attributes on the Melon object
        melon.quantity = session["cart"][melon_id]
        melon.cost = melon.price * session['cart'][melon_id]
    
    #    - add the Melon object to the list created above
        cart_melons.append(melon)
        
    # - pass the total order cost and the list of Melon objects to the template
    #
    # Make sure your function can also handle the case wherein no cart has
    # been added to the session

    return render_template("cart.html", total_cost=cart_subtotal, cart_melons=cart_melons)


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    # TODO: Need to implement this!

    # The logic here should be something like:
    #
    # - get user-provided name and password from request.form
    # - use customers.get_by_email() to retrieve corresponding Customer
    #   object (if any)
    # - if a Customer with that email was found, check the provided password
    #   against the stored one
    # - if they match, store the user's email in the session, flash a success
    #   message and redirect the user to the "/melons" route
    # - if they don't, flash a failure message and redirect back to "/login"
    # - do the same if a Customer with that email doesn't exist

    return "Oops! This needs to be implemented"


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=6060)
