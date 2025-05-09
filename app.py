import sqlite3,json

# Database setup function
# Database setup function
# Database setup function
import sqlite3
import json

# Function to add the updated_price column if it does not exist
def add_updated_price_column():
    conn = sqlite3.connect('closet_items.db')
    cursor = conn.cursor()

    # Check if the 'updated_price' column already exists in the 'closet_items' table
    cursor.execute("PRAGMA table_info(closet_items);")
    columns = cursor.fetchall()

    # Check if 'updated_price' column is already present
    if not any(column[1] == 'updated_price' for column in columns):
        # If not present, add the 'updated_price' column
        cursor.execute("ALTER TABLE closet_items ADD COLUMN updated_price REAL;")
        conn.commit()

    conn.close()

# Database setup function
def init_db():
    conn = sqlite3.connect('closet_items.db')
    cursor = conn.cursor()

    # Create a table for closet items if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS closet_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            color TEXT NOT NULL,
            price REAL NOT NULL,
            updated_price REAL,  -- Column for storing discounted price
            image_url TEXT NOT NULL,
            size TEXT NOT NULL,
            tags TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# Ensure the 'updated_price' column is added if missing
add_updated_price_column()  # Call this function once

# Call init_db function to create the table when the app starts
init_db()

# Other routes and logic for the app follow here...




def get_closet_items():
    conn = sqlite3.connect('closet_items.db')
    cursor = conn.cursor()

    # Fetch all closet items along with their updated_price
    cursor.execute('SELECT id, name, category, color, price, updated_price, image_url, size, tags FROM closet_items')
    rows = cursor.fetchall()

    closet_items = []
    for row in rows:
        item = {
             'id' : row[0],  # ✅ include real database ID
            'name': row[1],
            'category': row[2],
            'color': row[3],
            'price': row[4],
            'updated_price': row[5],
            'image_url': row[6],
            'size': row[7],
            'tags': json.loads(row[8]) # Tags are stored as JSON strings
        }
        closet_items.append(item)

    conn.close()
    return closet_items


import json
import os

# Function to save feedback to a JSON file
def save_feedback(feedback_data):
    feedback_file = 'feedback.json'

    # Load existing feedback data if the file exists
    if os.path.exists(feedback_file):
        with open(feedback_file, 'r') as f:
            feedbacks = json.load(f)
    else:
        feedbacks = []

    # Append the new feedback to the list
    feedbacks.append(feedback_data)

    # Save the updated feedback list back to the file
    with open(feedback_file, 'w') as f:
        json.dump(feedbacks, f, indent=4)


import json
import requests
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os

app = Flask(__name__)

app.secret_key = 'your_secret_key'  # Secret key for session management 
GEMINI_API_KEY = 'AIzaSyCsXTGxnJrfyOB-tTFtOmzR4XL6VaVSZ2k'

import requests

# Replace with your actual API key from OpenWeather
WEATHER_API_KEY = '151e737556cf2b3114c276208bb7cacc'

@app.route('/weather', methods=['GET', 'POST'])
def weather_suggestions():
    if request.method == 'POST':
        city = request.form['city']

        # Call OpenWeather API
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200 or 'main' not in data:
            return render_template('weather.html', city=city, weather="Unavailable", suggested_items=[])

        temp = data['main']['temp']
        weather_desc = data['weather'][0]['main'].lower()

        # Match weather to tags
        tags = []
        if temp > 30:
            tags.append('light')
        elif temp < 15:
            tags.append('warm')
        elif 'rain' in weather_desc:
            tags.append('rainy')
        else:
            tags.append('normal')

        # Fetch matching clothes
        closet_items = get_closet_items()
        suggested_items = [item for item in closet_items if any(tag in item.get('tags', []) for tag in tags)]

        return render_template('weather.html', city=city, weather=f"{temp}°C, {weather_desc}", suggested_items=suggested_items)

    return render_template('weather.html')









# Define the route for the chatbot
@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot_interface():
    if request.method == 'POST':
        user_mood = request.json.get('mood')  # Get the mood from the request body
        mood_tags = user_mood.split(",")  # Example user input: "happy, excited"

        # Fetch relevant items based on the mood tags
        closet_items = get_closet_items()
        relevant_items = fetch_closet_items_by_mood(mood_tags)

        # If no relevant items in wardrobe, suggest items from the closet
        if relevant_items:
            suggestions = relevant_items
        else:
            suggestions = closet_items  # If no matching wardrobe items, suggest all closet items

        # Return the filtered closet items as response to the frontend
        return jsonify({
            "message": f"Here are some clothing suggestions based on your mood: "
               f"{', '.join([f'{item['name']} <img src=\"{item['image_url']}\" alt=\"{item['name']}\" style=\"max-width: 100px; height: auto;\" />' for item in suggestions])}",
            "items": suggestions  # Send items as well
        })

    return render_template('chatbot.html')





# Function to fetch items based on mood tag
def fetch_closet_items_by_mood(mood_tags):
    closet_items = get_closet_items() # Fetch closet items from the database
    filtered_items = []
    for item in closet_items:
        if any(tag in item['tags'] for tag in mood_tags):
            filtered_items.append(item)
    return filtered_items


# Function to get AI (Gemini) response based on the user's mood input
def get_ai_response(user_mood):
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    # Send the user mood as input to the AI model
    data = {
        "prompt": f"Suggest clothing based on the mood: {user_mood}",
        "max_tokens": 150
    }
    response = requests.post("https://api.gemini.com/v1/completions", headers=headers, json=data)
    return response.json().get('choices')[0].get('text')
# OpenWeatherMap API details
## OpenWeatherMap API details

                

# Function to get clothing suggestion based on weather condition


import json
import os

USERS_FILE = 'users.json'

def load_users():
    if os.path.exists(USERS_FILE): 
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)
WARDROBE_FILE = 'wardrobe.json'

def load_wardrobe():
    if os.path.exists(WARDROBE_FILE):
        with open(WARDROBE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_wardrobe(wardrobe_data):
    with open(WARDROBE_FILE, 'w') as f:
        json.dump(wardrobe_data, f, indent=4)



@app.route('/remove_wardrobe_item', methods=['POST'])
def remove_wardrobe_item():
    if 'email' not in session:
        return redirect(url_for('login'))

    email = session['email']
    item_name = request.form['item_name']
    item_size = request.form['item_size']

    wardrobe_data = load_wardrobe()

    if email in wardrobe_data:
        wardrobe_data[email] = [
            item for item in wardrobe_data[email]
            if not (item['name'] == item_name and item.get('size') == item_size)
        ]
        save_wardrobe(wardrobe_data)

    session['success_message'] = f"'{item_name}' has been removed from your wardrobe."
    return redirect(url_for('dashboard'))





@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if email ends with @gmail.com
        if not email.endswith('@gmail.com'):
            error = "Email must be a Gmail address (e.g., yourname@gmail.com)."
            return render_template('register.html', error=error)

        users = load_users()

        # Check if email already registered
        if any(user['email'] == email for user in users):
            error = "This email is already registered. Please log in."
            return render_template('register.html', error=error)

        # Register the user
        users.append({'username': username, 'email': email, 'password': password})
        save_users(users)

        return redirect(url_for('login'))

    return render_template('register.html')




@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        users = load_users()

        # Find user in file
        user = next((u for u in users if u['email'] == email and u['password'] == password), None)

        if user:
            if user.get("banned", False):
                error = "You have been banned."
                return render_template('login.html', error=error)

            
            # Store the first name in the session
            first_name = user['username'].split()[0]  # Assuming the username is in the format "First Last"
            session['first_name'] = first_name  # Save the first name in the session
            session['username'] = user['username']
            session['email'] = user['email']

            return redirect(url_for('dashboard'))
        else:
            error = "Invalid email or password"
            return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_id = request.form['admin_id']
        admin_password = request.form['admin_password']

        # Check the admin credentials
        if admin_id == '21201344' and admin_password == '1234':
            session['is_admin'] = True
            session['admin_id'] = admin_id
            return redirect(url_for('admin_dashboard'))  # Redirect to the admin dashboard

        # Invalid credentials
        error = "Invalid Admin ID or Password"
        return render_template('admin_login.html', error=error)

    return render_template('admin_login.html')



@app.route('/admin_dashboard')
def admin_dashboard():
    if 'is_admin' not in session or not session['is_admin']:
        return redirect(url_for('login'))

    admin_id = session.get('admin_id')
    return render_template('admin_dashboard.html', admin_id=admin_id)



@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    email = session['email']

    wardrobe_data = load_wardrobe()
    wardrobe_items = wardrobe_data.get(email, [])

    return render_template('dashboard.html', username=username, wardrobe_items=wardrobe_items)



@app.route('/view_product_list', methods=['GET'])
def view_product_list():
    conn = sqlite3.connect('closet_items.db')
    cursor = conn.cursor()

    # ✅ Fetch actual IDs and updated prices directly from DB
    cursor.execute("SELECT id, name, category, color, price, updated_price FROM closet_items")
    rows = cursor.fetchall()
    conn.close()

    product_list = []
    for row in rows:
        product_list.append({
            'id': row[0],                 # ✅ Real product ID from database
            'name': row[1],
            'category': row[2],
            'color': row[3],
            'price': row[4],
            'updated_price': row[5]
        })

    return render_template('view_product_list.html', product_list=product_list)





@app.route('/closet', methods=['GET'])
def view_closet():
    if 'username' not in session :
        return redirect(url_for('login'))

    sort_by = request.args.get('sort_by', 'color')  # Default sorting is by color
    color_filter = request.args.get('color_filter', '')
    view_by = request.args.get('view_by', '')

    # Clear the success message if not related to cart operation
    success_message = session.pop('success_message', None)

    # Fetch items from the database
    closet_items = get_closet_items()

    # Filter items by color
    if color_filter:
        filtered_items = [item for item in closet_items if color_filter.lower() in item['color'].lower()]
    else:
        filtered_items = closet_items[:]

    # Filter by category or fabric
    if view_by == 'category':
        filtered_items = [item for item in filtered_items if item['category']]
    elif view_by == 'fabric':
        filtered_items = [item for item in filtered_items if 'fabric' in item]  # Optional

    # Sort items
    if sort_by == 'price':
        filtered_items.sort(key=lambda x: x['price'])
    else:
        filtered_items.sort(key=lambda x: x['color'])

    username = session.get('username')  # ✅ Grab the username from the session

    return render_template(
        'view_closet.html',
        closet_items=filtered_items,
        success_message=success_message,
        username=username ) # ✅ Send to template 
    


from urllib.parse import unquote  # Make sure to import unquote if not already imported

@app.route('/add_to_cart/<string:item_name>', methods=['POST'])
def add_to_cart(item_name):
    item_name = unquote(item_name)  # Decode URL-encoded name like Red%20Sweater → Red Sweater
    quantity = int(request.form.get('quantity', 1))
    size = request.form.get('size', 'medium')  # Get size from form (default to 'medium')

    # Find the item in the closet_items list
    closet_items = get_closet_items()  # Fetch closet items from the database
    item = next((i for i in closet_items if i['name'] == item_name), None)
    
    if not item:
        session['success_message'] = "Item not found."
        return redirect(url_for('view_closet'))

    if 'cart' not in session:
        session['cart'] = []

    # Add size to the item before adding to cart
    for cart_item in session['cart']:
        if cart_item['name'] == item['name'] and cart_item['size'] == size:  # Check both name and size
            cart_item['quantity'] += quantity  # If item already in cart, just update quantity
            break
    else:
        item_copy = item.copy()
        item_copy['quantity'] = quantity
        item_copy['size'] = size  # Add size to the item copy

        # Use the discounted price (updated_price), if available; otherwise, fallback to original price
        item_copy['price'] = item['updated_price'] if item['updated_price'] else item['price']
        
        session['cart'].append(item_copy)

    # Update the total price in the session
    session['total_price'] = sum(i['price'] * i['quantity'] for i in session['cart'])

    session['success_message'] = f"'{item['name']}' (Size: {size}) has been added to the cart!"
    return redirect(url_for('view_closet'))





@app.route('/view_cart', methods=['GET'])
def view_cart():
    cart_items = session.get('cart', [])
    total_price = session.get('total_price', 0.0)
    return render_template('view_cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/remove_from_cart/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    if 'cart' in session:
        session['cart'] = [item for idx, item in enumerate(session['cart']) if idx != item_id]
        session['total_price'] = sum(item['price'] * item['quantity'] for item in session['cart'])
        session['success_message'] = "Item removed successfully!"  # Success message for item removal
    return redirect(url_for('view_cart'))

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session.pop('cart', None)
    session.pop('total_price', None)
    session['success_message'] = "Cart cleared successfully!"  # Success message for clearing the cart
    return redirect(url_for('view_closet')) 


@app.route('/confirm_payment', methods=['POST'])
def confirm_payment():
    if 'username' not in session:
        return redirect(url_for('login'))

    email = session.get('email')  # Use the same email from login
    cart_items = session.get('cart', [])

    # Load current wardrobe data from file
    wardrobe_data = load_wardrobe()

    # If user already has wardrobe items, extend them
    if email in wardrobe_data:
        wardrobe_data[email].extend(cart_items)
    else:
        wardrobe_data[email] = cart_items

    # Save updated data
    save_wardrobe(wardrobe_data)

    # Clear cart
    session.pop('cart', None)
    session.pop('total_price', None)

    session['success_message'] = "Payment confirmed! Items moved to your wardrobe."

    return redirect(url_for('dashboard'))



# ================= VIEW CATEGORIES =================

@app.route('/view_categories', methods=['GET'])
def view_categories():
    return render_template('view_categories.html')

# ================= VIEW FABRICS =================

@app.route('/view_fabrics', methods=['GET'])
def view_fabrics():
    return render_template('view_fabrics.html')
@app.route('/fabric_instructions/<fabric>')
def fabric_instructions(fabric):
    # Fabric care instructions
    care_instructions = {
        'silk': 'Dry clean only. Do not bleach. Iron on low heat.',
        'cotton-silk': 'Hand wash in cold water. Do not wring. Iron on low heat.',
        'chiffon': 'Dry clean only. Do not tumble dry.',
        'georgette': 'Hand wash cold. Do not bleach.',
        # Add more fabric types here
    }

    # Get the specific instructions for the clicked fabric
    instructions = care_instructions.get(fabric, 'No instructions available for this fabric.')

    # Render a blank page to display the instructions
    return render_template('fabric_instructions.html', fabric=fabric, instructions=instructions)


@app.route('/logout')
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for('login'))

@app.route('/quick_view/<item_name>')
def quick_view(item_name):
    # Find the item in closet_items
    closet_items = get_closet_items()  # Fetch closet items from the database
    item = next((i for i in closet_items if i['name'] == item_name), None)
    if item:
        return render_template('quick_view.html', item=item)
    else:
        return redirect(url_for('view_closet'))  # If item is not found

@app.route('/chatbot')
def chatbot_page():
    return render_template('chatbot.html')  # Make sure you have a chatbot.html template



@app.route('/apply_discount/<string:selected_product>/<int:discount_percent>', methods=['GET'])
def apply_discount(selected_product, discount_percent):
    conn = sqlite3.connect('closet_items.db')
    cursor = conn.cursor()

    if selected_product == 'all':
        cursor.execute("SELECT id, price FROM closet_items")
        products = cursor.fetchall()

        for product_id, price in products:
            updated_price = price * (1 - discount_percent / 100)
            cursor.execute("UPDATE closet_items SET updated_price = ? WHERE id = ?", (updated_price, product_id))
    else:
        product_id = int(selected_product)
        cursor.execute("SELECT price FROM closet_items WHERE id = ?", (product_id,))
        row = cursor.fetchone()
        if row:
            price = row[0]
            updated_price = price * (1 - discount_percent / 100)
            cursor.execute("UPDATE closet_items SET updated_price = ? WHERE id = ?", (updated_price, product_id))

    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": f"{discount_percent}% discount applied."})


@app.route('/submit_feedback')
def submit_feedback(): 
    return render_template('submit_feedback.html')


@app.route('/submit_feedback', methods=['POST'])
def submit_feedback_action():
    # Get the form data
    full_name = request.form['full_name']
    feedback = request.form['feedback']
    rating = request.form.get('rating', None)

    # Prepare feedback data
    feedback_data = {
        'name': full_name,
        'feedback': feedback,
        'rating': rating
    }

    # Store feedback data
    save_feedback(feedback_data)

    # Display a success message
    session['success_message'] = 'Thank you for your feedback!'
    return redirect(url_for('dashboard'))



@app.route('/view_feedback')
def view_feedback():
    # Load feedback from the JSON file
    feedback_file = 'feedback.json'
    if os.path.exists(feedback_file):
        with open(feedback_file, 'r') as f:
            feedbacks = json.load(f)
    else:
        feedbacks = []

    # Render a template to display the feedback in a table
    return render_template('view_feedback.html', feedbacks=feedbacks)
from flask import request, redirect, url_for, render_template
import sqlite3
import json

# Route for displaying the Add Product page
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        # Get data from the form
        name = request.form['name']
        category = request.form['category']
        color = request.form['color']
        price = float(request.form['price'])
        image_url = request.form['image_url']
        size = request.form['size']
        tags = request.form['tags'].split(",")  # Tags are entered as a comma-separated string

        # Connect to the database
        conn = sqlite3.connect('closet_items.db')
        cursor = conn.cursor()

        # Insert the new product into the database
        cursor.execute('''
            INSERT INTO closet_items (name, category, color, price, image_url, size, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, category, color, price, image_url, size, json.dumps(tags)))

        # Commit and close the connection
        conn.commit()
        conn.close()

        # Redirect to the admin dashboard or product list
        return redirect(url_for('admin_dashboard'))

    return render_template('add_product.html')

from flask import render_template, request, redirect, url_for
import sqlite3


@app.route('/remove_product', methods=['GET', 'POST'])
def remove_product():
    if 'is_admin' not in session or not session['is_admin']:
        return redirect(url_for('login'))

    conn = sqlite3.connect('closet_items.db')
    cursor = conn.cursor()

    # Fetch all the product names (assuming 'name' is unique)
    cursor.execute("SELECT DISTINCT name FROM closet_items")
    products = cursor.fetchall()

    if request.method == 'POST':
        product_name = request.form['product_name']
        
        # Remove the product by name (unique)
        cursor.execute("DELETE FROM closet_items WHERE name = ?", (product_name,))
        conn.commit()

        session['success_message'] = f"Product '{product_name}' has been removed!"
        return redirect(url_for('remove_product'))

    conn.close()
    return render_template('remove_product.html', products=products)



@app.route('/update_product', methods=['GET', 'POST'])
def update_product():
    if 'is_admin' not in session or not session['is_admin']:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        product_name = request.form['product_name']
        new_price = request.form['new_price']
        new_color = request.form['new_color']
        new_size = request.form['new_size']
        new_image_url = request.form['new_image_url']

        # Connect to the database and update the product
        conn = sqlite3.connect('closet_items.db')
        cursor = conn.cursor()

        # Fetch the current category of the product before updating
        cursor.execute("SELECT category FROM closet_items WHERE name = ?", (product_name,))
        current_category = cursor.fetchone()[0]  # Get the current category

        # Now update only the necessary fields (price, color, size, and image_url)
        cursor.execute("""
            UPDATE closet_items
            SET price = ?, color = ?, updated_price = ?, image_url = ?, size = ?
            WHERE name = ? AND category = ?
        """, (new_price, new_color, new_price, new_image_url, new_size, product_name, current_category))

        conn.commit()
        conn.close()

        return redirect(url_for('view_product_list'))  # Redirect to the product list after update

    # Fetch all products to display in the dropdown
    closet_items = get_closet_items()
    return render_template('update_product.html', closet_items=closet_items)



@app.route('/add_to_favourite', methods=['POST'])
def add_to_favourite():
    if 'email' not in session:
        return redirect(url_for('login'))

    email = session['email']
    item_name = request.form['item_name']
    item_size = request.form['item_size']

    wardrobe_data = load_wardrobe()

    # Find and update the item
    if email in wardrobe_data:
        for item in wardrobe_data[email]:
            if item['name'] == item_name and item.get('size') == item_size:
                if 'favourite' not in item.get('tags', []):
                    item.setdefault('tags', []).append('favourite')
        save_wardrobe(wardrobe_data)

    session['success_message'] = f"'{item_name}' added to favourites."
    return redirect(url_for('dashboard'))


@app.route('/profile', methods=['GET'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    users = load_users()
    email = session['email']
    user = next((u for u in users if u['email'] == email), None)

    if not user:
        return redirect(url_for('login'))

    return render_template('profile.html', user=user)


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    users = load_users()
    email = session['email']
    user = next((u for u in users if u['email'] == email), None)

    if not user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_username = request.form['username']
        new_email = request.form['email']
        new_password = request.form['password']

        # Update user in list
        user['username'] = new_username
        user['email'] = new_email
        if new_password:  # Only update password if it's not empty
            user['password'] = new_password

        save_users(users)
        session['username'] = new_username
        session['email'] = new_email

        return redirect(url_for('profile'))

    return render_template('edit_profile.html', user=user)


@app.route('/view_favourites')
def view_favourites():
    if 'email' not in session:
        return redirect(url_for('login'))

    email = session['email']
    wardrobe_data = load_wardrobe()
    favourites = []

    if email in wardrobe_data:
        favourites = [item for item in wardrobe_data[email] if 'favourite' in item.get('tags', [])]

    return render_template('view_favourites.html', favourites=favourites)


action="{{ url_for('ban_user') }}"
action="{{ url_for('unban_user') }}"


@app.route('/manage_users', methods=['GET', 'POST'])
def manage_users():
    if 'is_admin' not in session or not session['is_admin']:
        return redirect(url_for('login'))

    users = load_users()

    if request.method == 'POST':
        action = request.form['action']
        email = request.form['email']

        for user in users:
            if user['email'] == email:
                if action == 'ban':
                    user['banned'] = True
                elif action == 'unban':
                    user['banned'] = False
                break
        save_users(users)

    return render_template('manage_users.html', users=users)

@app.route('/ban_user', methods=['POST'])
def ban_user():
    email = request.form['email']
    users = load_users()
    for user in users:
        if user['email'] == email:
            user['banned'] = True
    save_users(users)
    return redirect(url_for('manage_users'))

@app.route('/unban_user', methods=['POST'])
def unban_user():
    email = request.form['email']
    users = load_users()
    for user in users:
        if user['email'] == email:
            user['banned'] = False
    save_users(users)
    return redirect(url_for('manage_users'))





if __name__ == '__main__':
    app.run(port=1344, debug=True)


