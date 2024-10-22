
import mysql.connector
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from passlib.hash import sha256_crypt
import hashlib
import gc
from functools import wraps
import webbrowser
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
from flask import after_this_request
from flask import request
from flask import flash
from mysql.connector import Error
from datetime import datetime



# Define the database configuration
db_config = {
    "host": "localhost",
    "user": "gunslinger",
    "password": "mohamed12345",
    "database": "horizon"
}
def get_connection():
    return mysql.connector.connect(**db_config)

conn = get_connection()

app = Flask(__name__)
app.secret_key = 'ironmike'


def get_menu_items():
    # Establish a database connection
    conn = get_connection()
    # Create a cursor object
    cursor = conn.cursor(dictionary=True)

    # Query the database for menu items
    cursor.execute("SELECT * FROM menu")

    # Fetch all menu items
    menu_items = cursor.fetchall()

    # Close cursor and connection
    cursor.close()
    conn.close()

    return menu_items

def get_restaurants():

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM restaurant")

  
    restaurants = cursor.fetchall()

 
    cursor.close()
    conn.close()

    return restaurants

def get_customer_names():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT Full_name FROM customer")  

    customer_names = [row['Full_name'] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return customer_names

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    error = ''
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['password_confirm']

       
        if name and email and password and password_confirm:
            if password == password_confirm:
                conn = get_connection()  
                if conn is not None:
                    try:
                        if conn.is_connected():
                            print('MySQL Connection is established')
                            dbcursor = conn.cursor()

                            hashed_password = sha256_crypt.hash(str(password))

                          
                            dbcursor.execute("INSERT INTO accounts (Email, hashed_password) VALUES (%s, %s)", (email, hashed_password))
                            conn.commit()

                            
                            user_type = request.form['user_type']
                            user_id = None
                            if user_type == 'staff':
                                dob = request.form['dob']  
                                gender = request.form['gender'] 
                                default_staff_type = 'staff'
                                dbcursor.execute("INSERT INTO Staff (Full_name, staff_type, DOB, Gender) VALUES (%s, %s, %s, %s)", (name, default_staff_type, dob, gender))
                                conn.commit()
                                staff_id = dbcursor.lastrowid  
                                print("Staff ID:", staff_id)

                            else:
                                dbcursor.execute("INSERT INTO Customer (Full_name) VALUES (%s)", (name,))
                                conn.commit()
                                user_id = dbcursor.lastrowid 

                       
                            if user_type == 'staff':
                                print("Staff ID:", staff_id)
                                dbcursor.execute("UPDATE accounts SET staff_id = %s WHERE Email = %s", (staff_id, email))
                            else:
                                print("Customer ID:", user_id)
                                dbcursor.execute("UPDATE accounts SET customer_id = %s WHERE Email = %s", (user_id, email))
                            conn.commit()

                            print(dbcursor.rowcount, "Thank you for registering!")
                            dbcursor.close()
                            conn.close()
                            return render_template("login.html", message='User registered successfully, please log in.')
                    except Error as e:
                        error = 'Error: Could not connect to the database'
                        print(error, e)
                    finally:
                        if conn.is_connected():
                            dbcursor.close()
                            conn.close()
                else:
                    error = 'Error: Could not establish database connection'
            else:
                error = 'Error: Passwords do not match'
        else:
            error = 'Error: Please fill in all required fields'

    return render_template('register.html', error=error)



def authenticate_user(email, password):
    try:
        conn = get_connection()
        if conn:
            if conn.is_connected():
                cursor = conn.cursor()
                
             
                cursor.execute("SELECT customer_id, staff_id, hashed_password FROM accounts WHERE Email = %s", (email,))
                account_data = cursor.fetchone()
                
                if account_data:
                
                    hashed_password = account_data[2]
                    if sha256_crypt.verify(password, hashed_password):
                        customer_id, staff_id = account_data[0], account_data[1]
                        if customer_id:
                
                            return True, 'customer'
                        elif staff_id:
    
                            return True, 'staff'
                        else:
                           
                            return False, None
                    else:
           
                        return False, None
                else:
                
                    return False, None
    except Exception as e:
        print("Error during authentication:", e)
    finally:
        cursor.close()
        conn.close()


    return False, None

def get_staff_type(email, password):
    try:
        conn = get_connection()
        if conn and conn.is_connected():
            cursor = conn.cursor()

           
            cursor.execute("SELECT staff_id FROM accounts WHERE Email = %s", (email,))
            account_data = cursor.fetchone()

            if account_data:
                staff_id = account_data[0]

            
                cursor.execute("SELECT staff_type FROM staff WHERE staff_id = %s", (staff_id,))
                staff_data = cursor.fetchone()

                if staff_data:
                    staff_type = staff_data[0]
                    return staff_type  # Return the staff type

    except Exception as e:
        print("Error during staff type retrieval:", e)
    finally:
        cursor.close()
        conn.close()
    return None 

def get_staff_type(email):
    try:
        conn = get_connection()
        if conn and conn.is_connected():
            cursor = conn.cursor()

            
            cursor.execute("SELECT staff_id FROM accounts WHERE Email = %s", (email,))
            account_data = cursor.fetchone()

            if account_data:
                staff_id = account_data[0]

        
                cursor.execute("SELECT staff_type FROM staff WHERE staff_id = %s", (staff_id,))
                staff_data = cursor.fetchone()

                if staff_data:
                    staff_type = staff_data[0]
                    return staff_type  

    except Exception as e:
        print("Error during staff type retrieval:", e)
    finally:
        cursor.close()
        conn.close()
    return None



@app.route('/login', methods=["GET","POST"])
def login():
    error = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        
        authenticated_user, user_type = authenticate_user(email, password)
        
        if authenticated_user:
            session['logged_in'] = True
            session['user_type'] = user_type 
            if user_type == 'customer':
                return redirect(url_for('customer_page'))  
            elif user_type == 'staff':
                staff_type = get_staff_type(email)
                if staff_type == 'staff':
                    return redirect(url_for('staff'))
                elif staff_type == 'manager':
                    session['user_type'] = 'manager'  # Set user_type as manager
                    return redirect(url_for('manager'))
                elif staff_type == 'admin':
                    session['user_type'] = 'admin' 
                    return redirect(url_for('admin'))
        else:
            error = 'Invalid email or password. Please try again.'

    return render_template('login.html', error=error)



def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:            
            print("You need to login first")
            return render_template('login.html', error='You need to login first')    
    return wrap

@app.route("/logout/")
def logout():    
    session.clear()   
    print("You have been logged out!")
    gc.collect()
    return render_template('index.html', optionalmessage='You have been logged out')

def customer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session and session.get('user_type') == 'customer':
            return f(*args, **kwargs)
        else:
            print("You need to login first as a customer")
            return render_template('login.html', error='You need to login first as a customer')    
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session and session.get('user_type') == 'admin':
            return f(*args, **kwargs)
        else:
            print("You need to login first as an admin user")
            return render_template('login.html', error='You need to login first as an admin user')    
    return decorated_function

def staff_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session and session.get('user_type') == 'staff':
            return f(*args, **kwargs)
        else:
            print("You need to login first as a staff member")
            return render_template('login.html', error='You need to login first as a staff member')    
    return decorated_function

def manager_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session and session.get('user_type') == 'manager':
            return f(*args, **kwargs)
        else:
            print("You need to login first as a manager")
            return render_template('login.html', error='You need to login first as a manager')    
    return decorated_function 


@login_required
@customer_required
@app.route('/order')
#@login_required
#@customer_required
def order():
    restaurants = get_restaurants()
    return render_template('order.html', menu=get_menu_items(), restaurants=restaurants)

@login_required
@customer_required
@app.route('/place_order', methods=['POST'])
def place_order():
    # Get form data
    main_id = int(request.form.get('starter'))
    dessert_id = int(request.form.get('dessert'))
    drink_id = int(request.form.get('drink'))
    main_quantity = int(request.form.get('main_quantity'))
    dessert_quantity = int(request.form.get('dessert_quantity'))
    drink_quantity = int(request.form.get('drink_quantity'))
    branch_id = int(request.form.get('branch_id'))

    menu_items = get_menu_items()

   
    restaurants = get_restaurants()

  
    main_item = next((item for item in menu_items if item['menu_id'] == main_id), None)
    dessert_item = next((item for item in menu_items if item['menu_id'] == dessert_id), None)
    drink_item = next((item for item in menu_items if item['menu_id'] == drink_id), None)

    # Find selected restaurant
    selected_restaurant = next((restaurant for restaurant in restaurants if restaurant['branch_id'] == branch_id), None)

    # Calculate total price
    total_price = (main_item['price'] * main_quantity) + (dessert_item['price'] * dessert_quantity) + (drink_item['price'] * drink_quantity)

    # Prepare data to pass to confirmation page
    order_data = {
        'main_item': main_item,
        'dessert_item': dessert_item,
        'drink_item': drink_item,
        'main_quantity': main_quantity,
        'dessert_quantity': dessert_quantity,
        'drink_quantity': drink_quantity,
        'total_price': total_price,
        'restaurant': selected_restaurant  # Pass selected restaurant information
    }

    # Store order data in session
    session['order_data'] = order_data

    # Return confirmation page with order data
    return render_template('confirmation.html', order_data=order_data)


@login_required
@customer_required
@app.route('/confirmation')
def confirm():
    order_data = session.get('order_data') 

    print("Order Data in Confirmation Page:", order_data)  

    if request.referrer and 'edit-item' in request.referrer:
        # Redirect to the order page with the order details
        if order_data:
            return redirect(url_for('order', **order_data))
        else:
            return redirect(url_for('index'))  
    else:
        return render_template('confirmation.html', order_data=order_data)

@login_required
@customer_required
@app.route('/edit_order', methods=['POST'])
def edit_order():
    # Retrieve the edited order data from the form
    edited_main_item = request.form.get('main-item')
    edited_dessert_item = request.form.get('dessert-item')
    edited_drink_item = request.form.get('drink-item')
    edited_main_quantity = request.form.get('main-quantity')
    edited_dessert_quantity = request.form.get('dessert-quantity')
    edited_drink_quantity = request.form.get('drink-quantity')


    order_data = session.get('order_data')


    menu_items = get_menu_items()
    restaurants = get_restaurants()


    return render_template('edit_order.html', order_data=order_data, menu=menu_items, restaurants=restaurants)

@login_required
@manager_required
@app.route('/menu_management')
def menu_management():
    menu_items = get_menu_items()

    
    return render_template('menu_management.html', menu_items=menu_items)

@login_required
@manager_required
def update_menu_item(menu_id, menu_name, menu_type, price):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    sql = "UPDATE menu SET menu_name = %s, menu_type = %s, price = %s WHERE menu_id = %s"

    cursor.execute(sql, (menu_name, menu_type, price, menu_id))
    conn.commit() 
    cursor.close()
    conn.close()

@login_required
@manager_required
@app.route('/edit_menu/<int:menu_id>', methods=['GET', 'POST'])
def edit_menu(menu_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM menu WHERE menu_id = %s", (menu_id,))
    menu_item = cursor.fetchone()
    cursor.close()
    conn.close()

    if request.method == 'POST':
       
        menu_name = request.form['menu_name']
        menu_type = request.form['menu_type']
        price = request.form['price']
   
        update_menu_item(menu_id, menu_name, menu_type, price)
        return redirect(url_for('menu_management'))

    return render_template('edit_menu.html', menu_item=menu_item)

@login_required
@manager_required
@app.route('/delete_menu/<int:menu_id>', methods=['POST'])
def delete_menu(menu_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    try:
        # Delete the menu item with the specified menu_id from the database
        cursor.execute("DELETE FROM menu WHERE menu_id = %s", (menu_id,))
        conn.commit()
        return "Menu item deleted successfully", 200
    except Exception as e:
        conn.rollback()
        return str(e), 500
    finally:
        cursor.close()
        conn.close()

@login_required
@manager_required
@app.route('/add_menu', methods=['GET', 'POST'])
def add_menu():
    if request.method == 'POST':
        # Retrieve form data for the new menu item
        menu_name = request.form['menu_name']
        menu_type = request.form['menu_type']
        price = request.form['price']
        
        # Check if the menu item already exists
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        sql = "SELECT COUNT(*) FROM menu WHERE menu_name = %s"
        cursor.execute(sql, (menu_name,))
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        if count > 0:
            error_message = "Menu item '{}' already exists.".format(menu_name)
            return render_template('add_menu.html', error_message=error_message)

  
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        sql = "INSERT INTO menu (menu_name, menu_type, price) VALUES (%s, %s, %s)"
        cursor.execute(sql, (menu_name, menu_type, price))
        conn.commit()
        cursor.close()
        conn.close()
        
        # Redirect to the menu management page after adding the menu item
        return redirect(url_for('menu_management'))


    return render_template('add_menu.html')


@app.route('/customer')
@login_required
@customer_required
def customer_page():
    if session.get('logged_in') and session.get('user_type') == 'customer':
        return render_template('customer.html')
    else:
        return redirect(url_for('login'))
   

@app.route('/staff')
@login_required
@staff_required
def staff():
    if session.get('logged_in') and session.get('user_type') == 'staff':
        return render_template('staff.html')
    else:
         return redirect(url_for('login'))

@app.route('/admin')
@login_required
@admin_required
def admin():
    if session.get('logged_in') and session.get('user_type') == 'admin':
        return render_template('admin.html')
    else:
        return redirect(url_for('login'))

@app.route('/manager')
@login_required
@manager_required
def manager():
    if session.get('logged_in') and session.get('user_type') == 'manager':
        return render_template('manager.html')
    else:
        return redirect(url_for('login'))

@login_required
@customer_required   
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        # Check if the form contains payment information
        if 'card-number' in request.form and 'expiration' in request.form and 'cvv' in request.form and 'name' in request.form:
            # Retrieve order data from the session
            order_data = session.get('order_data')

            # Extract relevant information from order_data
            main_item_id = order_data['main_item']['menu_id']
            main_quantity = order_data['main_quantity']
            main_price = order_data['main_item']['price']
            dessert_item_id = order_data['dessert_item']['menu_id']
            dessert_quantity = order_data['dessert_quantity']
            dessert_price = order_data['dessert_item']['price']
            drink_item_id = order_data['drink_item']['menu_id']
            drink_quantity = order_data['drink_quantity']
            drink_price = order_data['drink_item']['price']
            total_price = order_data['total_price']

            try:
                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute("INSERT INTO orders (menu_id, quantity, new_price) VALUES (%s, %s, %s)", (main_item_id, main_quantity, main_price))
                cursor.execute("INSERT INTO orders (menu_id, quantity, new_price) VALUES (%s, %s, %s)", (dessert_item_id, dessert_quantity, dessert_price))
                cursor.execute("INSERT INTO orders (menu_id, quantity, new_price) VALUES (%s, %s, %s)", (drink_item_id, drink_quantity, drink_price))

                conn.commit()

                cursor.close()
                conn.close()

                # Return JavaScript to display alert without redirecting
                return """
                <script>
                    alert("Payment successful!");
                </script>
                """

            except Exception as e:
                print("Error inserting order details into the database:", e)
                return jsonify({'error': 'Payment failed. Please try again.'})
        
    # If the request method is GET or payment fails, render the payment page
    return render_template('payment.html')



def get_customer_id_by_name(customer_name):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT Customer_id FROM customer WHERE Full_name = %s", (customer_name,))
        result = cursor.fetchone()  # Fetch the first result

        if result:
            customer_id = result[0]
        else:
            customer_id = None

        cursor.close()
        conn.close()

        return customer_id

    except Exception as e:
        print("Error retrieving customer ID:", e)
        return None

@login_required
@manager_required
@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        # Get form data
        branch_id = request.form.get('branch_id')
        customer_name = request.form.get('customer_name')  # Get customer name from the form
        reservation_date = request.form.get('reservation_date')
        reservation_time = request.form.get('reservation_time')
        reservation_type = request.form.get('reservation_type')
        number_of_guests = request.form.get('number_of_guests')

        branch_name = get_restaurants()
        customer_id = get_customer_id_by_name(customer_name)
     
        if customer_id is None:
            return "Customer not found. Please make sure the name is correct."

        
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            cursor.execute("INSERT INTO reservation (reservation_date, reservation_type, number_of_guests, customer_id, branch_id) VALUES (%s, %s, %s, %s, %s)", (reservation_date, reservation_type, number_of_guests, customer_id, branch_id))

            conn.commit()

            cursor.close()
            conn.close()

            return "Reservation booked successfully!"  

        except Exception as e:
            print("Error inserting reservation into the database:", e)
            return "Failed to book reservation. Please try again."


    restaurants = get_restaurants()
    customers = get_customer_names()
    return render_template('reservation.html', restaurants=restaurants, customers=customers)


def get_reservation_data():
    try:
       
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
     
        query = """
            SELECT 
                r.reservation_id, 
                r.reservation_date, 
                r.reservation_type, 
                r.number_of_guests, 
                c.Full_name AS customer_name, 
                re.restaurant_name, 
                re.restaurant_location
            FROM 
                reservation AS r
            JOIN 
                Customer AS c ON r.customer_id = c.Customer_id
            JOIN 
                restaurant AS re ON r.branch_id = re.branch_id
        """
        
    
        cursor.execute(query)
        
        # Fetch all 
        reservation_data = cursor.fetchall()
        

        cursor.close()
        conn.close()
        
        return reservation_data
    
    except Exception as e:
        print("Error:", e)
        return None

def get_reservation_data_by_id(reservation_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT r.reservation_id, r.reservation_date, r.reservation_type, r.number_of_guests, c.Full_name AS customer_name, re.restaurant_name, re.restaurant_location FROM reservation AS r JOIN Customer AS c ON r.customer_id = c.Customer_id JOIN restaurant AS re ON r.branch_id = re.branch_id WHERE reservation_id = %s", (reservation_id,))
        reservation_data = cursor.fetchone()

        cursor.close()
        conn.close()

        return reservation_data
    except Exception as e:
        print("Error retrieving reservation data:", e)
        return None

def get_restaurant_names():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT restaurant_name FROM restaurant")

        restaurant_names = [row[0] for row in cursor.fetchall()] # Fetch all restaurant names

        cursor.close()
        conn.close()

        return restaurant_names
    except Exception as e:
        print("Error retrieving restaurant names:", e)
        return []


@login_required
@manager_required
@app.route('/reservation_management')
def reservation_management():
    reservation_data = get_reservation_data()
    
    return render_template('reservation_management.html', reservation_data=reservation_data)

def get_branch_id_by_name(restaurant_name):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT branch_id FROM restaurant WHERE restaurant_name = %s", (restaurant_name,))
        branch_id = cursor.fetchone()

        cursor.close()
        conn.close()

        if branch_id:
            return branch_id[0]
        else:
            return None

    except Exception as e:
        print("Error retrieving branch ID:", e)
        return None

@login_required
@manager_required
@app.route('/edit_reservation/<int:reservation_id>', methods=['GET', 'POST'])
def edit_reservation(reservation_id):
    if request.method == 'GET':
        reservation_data = get_reservation_data_by_id(reservation_id)
        if reservation_data:
            customers = get_customer_names()
            restaurants = get_restaurant_names()
            reservation_data['formatted_reservation_datetime'] = reservation_data['reservation_date'].strftime('%Y-%m-%dT%H:%M')
            return render_template('edit_reservation.html', reservation_data=reservation_data, customers=customers, restaurants=restaurants)
        else:
            return "Reservation not found", 404
    elif request.method == 'POST':

        restaurant_name = request.form.get('branch_id')
        customer_name = request.form.get('customer_name')
        reservation_date = request.form.get('reservation_date')
        reservation_type = request.form.get('reservation_type')
        number_of_guests = request.form.get('number_of_guests')

        # Convert restaurant name to branch ID
        branch_id = get_branch_id_by_name(restaurant_name)
        if branch_id is None:
            return "Restaurant not found. Please make sure the name is correct."

        customer_id = get_customer_id_by_name(customer_name)
      
        if customer_id is None:
            return "Customer not found. Please make sure the name is correct."

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            cursor.execute("UPDATE reservation SET reservation_date = %s, reservation_type = %s, number_of_guests = %s, customer_id = %s, branch_id = %s WHERE reservation_id = %s", (reservation_date, reservation_type, number_of_guests, customer_id, branch_id, reservation_id))

            conn.commit()

            cursor.close()
            conn.close()

            return "Reservation updated successfully!" 

        except Exception as e:
            print("Error updating reservation in the database:", e)
            return "Failed to update reservation. Please try again."
@login_required
@manager_required
@app.route('/delete_reservation/<int:reservation_id>', methods=['POST'])
def delete_reservation(reservation_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM reservation WHERE reservation_id = %s", (reservation_id,))
        conn.commit()

        cursor.close()
        conn.close()

        return "Reservation deleted successfully!"

    except Exception as e:
        print("Error deleting reservation:", e)
        return "Failed to delete reservation. Please try again."

def get_inventory():

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM inventory")

  
    inventory = cursor.fetchall()

 
    cursor.close()
    conn.close()

    return inventory

@login_required
@staff_required
@app.route('/inventory')
def inventory_management():
    inventory_items = get_inventory() 
    return render_template('inventory.html', inventory=inventory_items)

@login_required
@staff_required
@app.route('/edit_inventory/<int:inventory_id>', methods=['GET', 'POST'])
def edit_inventory(inventory_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
    
        inventory_name = request.form['inventory_name']
        inventory_quantity = request.form['inventory_quantity']


        cursor.execute("UPDATE inventory SET inventory_name = %s, inventory_quantity = %s WHERE inventory_id = %s",
                       (inventory_name, inventory_quantity, inventory_id))
        conn.commit()

    
        cursor.close()
        conn.close()

        return redirect(url_for('inventory_management'))

    else:

        cursor.execute("SELECT * FROM inventory WHERE inventory_id = %s", (inventory_id,))
        inventory_item = cursor.fetchone()


        cursor.close()
        conn.close()


        return render_template('edit_inventory.html', inventory_item=inventory_item)

@login_required
@staff_required
@app.route('/add_inventory', methods=['GET', 'POST'])
def add_inventory():
    if request.method == 'POST':

        inventory_name = request.form['inventory_name']
        inventory_quantity = request.form['inventory_quantity']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()


        cursor.execute("INSERT INTO inventory (inventory_name, inventory_quantity) VALUES (%s, %s)", (inventory_name, inventory_quantity))
        conn.commit()

        cursor.close()
        conn.close()


        return redirect(url_for('inventory_management'))
    else:

        return render_template('add_inventory.html')
@login_required
@staff_required
@app.route('/delete_inventory/<int:inventory_id>', methods=['POST'])
def delete_inventory(inventory_id):
    if request.method == 'POST':
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            cursor.execute("DELETE FROM inventory WHERE inventory_id = %s", (inventory_id,))
            conn.commit()

            cursor.close()
            conn.close()

            return "Inventory item deleted successfully!"

        except Exception as e:
            print("Error deleting inventory item:", e)
            return "Failed to delete inventory item. Please try again."
        
def get_customer_details():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Customer")
    customer_details = cursor.fetchall()


    cursor.close()
    conn.close()


    return customer_details,

def get_staff_details():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM staff")
    staff_details = cursor.fetchall()

    cursor.close()
    conn.close()

    return staff_details

@login_required
@admin_required
@app.route('/staff_managment')
def staff_management():
    staff_details = get_staff_details() 
    return render_template('staff_managment.html', staff=staff_details)

@login_required
@admin_required
@app.route('/edit_staff/<int:staff_id>', methods=['GET', 'POST'])
def edit_staff(staff_id):
    if request.method == 'POST':
        full_name = request.form['full_name']
        dob = request.form['dob']
        gender = request.form['gender']
        staff_type = request.form['staff_type']

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE staff
                SET Full_name = %s, DOB = %s, Gender = %s, staff_type = %s
                WHERE staff_id = %s
            """, (full_name, dob, gender, staff_type, staff_id))
            conn.commit()

            cursor.close()
            conn.close()

            return redirect(url_for('staff_management'))  

        except mysql.connector.Error as err:
            print("Error updating staff member:", err)
            return "Failed to update staff member. Please try again."

    else:
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)


            cursor.execute("SELECT * FROM staff WHERE staff_id = %s", (staff_id,))
            staff_member = cursor.fetchone()

            cursor.close()
            conn.close()

            return render_template('edit_staff.html', staff_member=staff_member)

        except mysql.connector.Error as err:
            print("Error retrieving staff member details:", err)
            return "Failed to retrieve staff member details. Please try again."

@login_required
@admin_required
@app.route('/delete_staff/<int:staff_id>', methods=['POST'])
def delete_staff(staff_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Delete the staff member from the accounts table
        cursor.execute("DELETE FROM accounts WHERE staff_id = %s", (staff_id,))
        
        # Delete the staff member from the staff table
        cursor.execute("DELETE FROM staff WHERE staff_id = %s", (staff_id,))
        
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for('staff_management'))  # Redirect to view staff page after deleting

    except mysql.connector.Error as err:
        print("Error deleting staff member:", err)
        return "Failed to delete staff member. Please try again."


if __name__ == '__main__':
    app.run(port=5022)
