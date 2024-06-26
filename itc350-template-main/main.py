import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from dotenv import load_dotenv
import bcrypt

# Load environment variables from .env file
load_dotenv()

# Initialize the flask app
app = Flask(__name__)
app.secret_key = os.getenv("SECRET")


# hashes a password and returns the hashed password
def hash_password(password):
    salt = bcrypt.gensalt()  # Generate a salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)  # Hash the password
    return hashed_password


# ------------------------ BEGIN FUNCTIONS ------------------------ #
# Function to retrieve DB connection
def get_db_connection():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_DATABASE")
    )
    return conn


# Get all items from the "items" table of the db
def get_all_items():
    # Create a new database connection for each request
    conn = get_db_connection()  # Create a new database connection
    cursor = conn.cursor(buffered=True)  # Creates a cursor for the connection, you need this to do queries
    # Query the db
    query = (
        "SELECT ItemName, ItemCost, ItemBaseDamage, ItemBeefynessBonus,ItemSmartnessBonus, ItemSpeedinessBonus, ItemID "
        "FROM item")
    cursor.execute(query)
    # Get result and close
    result = cursor.fetchall()  # Gets result from query
    conn.close()  # Close the db connection
    # (NOTE: You should do this after each query, otherwise your database may become locked)
    return result


# This gets all characters from the database
def get_all_chars():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = ("SELECT CharacterFName, CharacterLName, CharacterBeefyness, CharacterBuffness, CharacterSmartness, "
             "CharacterSpeediness FROM characters")
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result


# this gets all users from the database
def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT Username, UserPassword, UserEmail FROM user"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result


# This inserts a User in the database
def insert_user(firstname, lastname, username, email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    query = "INSERT INTO user (UserFName, UserLName, UserEmail, UserPassword, Username) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (firstname, lastname, email, hashed_password, username))
    conn.commit()
    cursor.close()
    conn.close()


# This inserts a character in the database
def insert_char(firstname, lastname, beefiness, buffness, smartness, speediness, user_id, class_id, race_id):
    print("User ID:", user_id)  # Print user ID for debugging
    conn = get_db_connection()
    cursor = conn.cursor()
    query = ("INSERT INTO characters (CharacterFName, CharacterLName, CharacterBeefyness, CharacterBuffness, "
             "CharacterSmartness, CharacterSpeediness, UserID, ClassID, RaceID) VALUES (%s, %s, %s, %s, %s, %s, %s, "
             "%s, %s)")
    cursor.execute(query, (firstname, lastname, beefiness, buffness, smartness, speediness, user_id, class_id, race_id))
    conn.commit()
    cursor.close()
    conn.close()


# This gets the character INFO based on the character ID
def get_char(character_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM CharacterInfo WHERE CharacterID=%s"
    cursor.execute(query, (character_id,))
    result = cursor.fetchall()
    conn.close()
    return result


# This gets the inventory based on the character ID
def get_inventory(character_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM Inventory WHERE CharacterID=%s"
    cursor.execute(query, (character_id,))
    result = cursor.fetchall()
    conn.close()
    return result


# This gets the character ID using the Firstname and lastname of a character
def get_character_id(firstname, lastname):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT CharacterID FROM characters WHERE CharacterFName = %s AND CharacterLName = %s"
    cursor.execute(query, (firstname, lastname))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]  # Return the first column of the first row
    else:
        return None  # Return None if character not found


# Gets the character and attributes from database
def get_character(character_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = ("SELECT CharacterFName, CharacterLName, CharacterBeefyness, CharacterBuffness, "
             "CharacterSmartness, CharacterSpeediness, CharacterID FROM characters WHERE CharacterID = %s")
    cursor.execute(query, (character_id,))
    result = cursor.fetchone()
    conn.close()
    return result


# Returns the equipped items of a character
def get_equipped(character_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT EquippedItemID FROM characters WHERE CharacterID=%s"
    cursor.execute(query, (character_id,))
    result = cursor.fetchall()
    conn.close()
    return result


# Equips an item to a character
def equip(character_id, item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE characters SET EquippedItemID=%s WHERE CharacterID=%s"
    cursor.execute(query, (item_id, character_id))
    conn.commit()
    cursor.close()
    conn.close()


# Unequips an item from a character
def unequip(character_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE characters SET EquippedItemID=NULL WHERE CharacterID=%s"
    cursor.execute(query, (character_id,))
    conn.commit()
    cursor.close()
    conn.close()


# Checks both passwords
def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)


# Helper function to verify that the login password is hashed and is the same as the password in the database
def verify_login(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT UserPassword FROM user WHERE Username = %s"
    cursor.execute(query, (username,))
    hashed_password = cursor.fetchone()
    conn.close()
    if hashed_password:
        hashed_password = hashed_password[0]
        # Hash the provided password and compare it to the stored hashed password
        if verify_password(password, hashed_password.encode('utf-8')):  # Ensure hashed_password is encoded
            return True
    return False


# Function for getting the purse amount of a character from the database
def get_purse(character_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT CharacterPurse FROM characters WHERE CharacterID=%s"
    cursor.execute(query, (character_id,))
    result = cursor.fetchall()
    conn.close()
    return result


# Function for returning the inventory of a character
def check_inventory(char_id, item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM character_inventory WHERE CharacterID=%s AND ItemID=%s"
    cursor.execute(query, (char_id, item_id))
    result = cursor.fetchall()
    conn.close()
    if not result:
        return False
    return True


# Function for purchasing items to update the database
def purchase_items(char_id, item_id, cost):
    char_purse = int(get_purse(char_id)[0][0])
    cost = int(cost)
    print(char_purse)
    print(cost)
    if (char_purse - cost >= 0) and (not check_inventory(char_id, item_id)):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "UPDATE characters SET CharacterPurse=%s WHERE CharacterID=%s"
        cursor.execute(query, (char_purse - cost, char_id))
        conn.commit()
        query = "INSERT INTO character_inventory(ItemID, CharacterID) VALUES (%s, %s)"
        cursor.execute(query, (item_id, char_id))
        conn.commit()
        cursor.close()
        conn.close()


# Selling Items function to update the database
def sell_items(char_id, item_id, cost):
    char_purse = int(get_purse(char_id)[0][0])
    cost = int(cost)
    print(char_purse)
    print(cost)
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE characters SET CharacterPurse=%s WHERE CharacterID=%s"
    cursor.execute(query, (char_purse + cost, char_id))
    conn.commit()
    query = "DELETE FROM character_inventory WHERE ItemID=%s AND CharacterID=%s"
    cursor.execute(query, (item_id, char_id))
    conn.commit()
    cursor.close()
    conn.close()


# Helper function for getting the User ID
def get_user_id(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT UserID FROM user WHERE Username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()[0]
    conn.close()
    return result


# Helper function for getting users
def get_user_characters(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = ("SELECT CharacterFName, CharacterLName, CharacterBeefyness, CharacterBuffness, CharacterSmartness, "
             "CharacterSpeediness, CharacterID FROM characters WHERE UserID = %s")
    cursor.execute(query, (user_id,))
    user_characters = cursor.fetchall()
    conn.close()
    return user_characters


# Function for getting the race description
def get_race_desc(char_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = ("SELECT RaceDescription FROM characters LEFT JOIN race ON characters.RaceID = race.RaceID WHERE "
             "CharacterID = %s")
    cursor.execute(query, (char_id,))
    desc = cursor.fetchall()
    conn.close()
    return desc[0][0]


# function for selecting the class descriptions
def get_class_desc(char_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = ("SELECT ClassDescription FROM characters LEFT JOIN class ON characters.ClassID = class.ClassID "
             "WHERE CharacterID = %s")
    cursor.execute(query, (char_id,))
    desc = cursor.fetchall()
    conn.close()
    return desc[0][0]


# ------------------------ END FUNCTIONS ------------------------ #


# ------------------------ BEGIN ROUTES ------------------------ #
# EXAMPLE OF GET REQUEST
@app.route("/", methods=["GET"])
def home():
    if not session.get("logged_in"):
        return render_template("login.html")
    else:
        return redirect(url_for("view_all_characters"))  # return the page to be rendered


@app.route("/character/add", methods=["GET"])
def add_character():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    data = request.form  # The form returned will have data objects username and password which will then be stored.
    username = data["username"]
    password = data["password"]

    right_password = verify_login(username, password)
    if right_password:
        user_id = get_user_id(username)
        if user_id:  # All of these are session variables that will be stored and then later accessed.
            session["logged_in"] = True
            session["username"] = username
            session["user_id"] = user_id  # Store user ID in session
            flash("Login successful", "success")
            return redirect(url_for("home"))
        else:
            flash("Failed to retrieve user ID", "error")
            return render_template("login.html")
    else:
        flash("Invalid username or password", "error")
        return render_template("login.html")


@app.route("/logout", methods=["POST"])  # Logout method
def logout():
    session["logged_in"] = False  # Session variables are removed from the project
    session.pop("username", None)
    flash("Logged out successfully", "success")
    return redirect(url_for("home"))


@app.route("/register", methods=["GET", "POST"])  # The register endpoint is used to register a user
def register():
    if request.method == "POST":
        try:
            data = request.form
            firstname = data["firstname"]
            lastname = data["lastname"]
            username = data["username"]
            email = data["email"]
            password = data["password"]  # Gathering data from the form

            users = get_all_users()

            existing_users = [user[0] for user in users]
            if username in existing_users:  # If the username exists does not log in and store
                flash("Username already exists. Please choose a different one.", "warning")
                return render_template("register.html")

            existing_email = [user[2] for user in users]
            if email in existing_email:  # If the email exists it does not log in and store
                flash("Email already exists. Please choose a different one.", "warning")
                return render_template("register.html")

            insert_user(firstname, lastname, username, email, password)
            user_id = get_user_id(username)
            session["logged_in"] = True
            session["username"] = username
            session["user_id"] = user_id

            flash("Registration successful. You have been automatically logged in.", "success")
            return redirect(url_for("home"))  # If the registration is successful it returns the page for home

        except Exception as e:
            flash(f"An error occurred during registration: {str(e)}", "error")
            return redirect(url_for("register"))  # Exception handling in case something goes wrong
    else:
        return render_template("register.html")


# Character Info Page
@app.route("/characterinfo", methods=["GET"])
def view_character_stats():
    char_id = request.args.get('charID')
    return render_template("characterInfo.html", character=get_char(char_id)[0], race_desc=get_race_desc(char_id),
                           class_desc=get_class_desc(char_id),
                           equippedItem=get_equipped(request.args.get('charID'))[0][0])


# viewing the characters route
@app.route("/characters", methods=["GET"])
def view_all_characters():
    # Retrieve user ID from the session
    user_id = session.get("user_id")
    # Retrieve characters associated with the user ID
    user_characters = get_user_characters(user_id)
    return render_template("character.html", user_characters=user_characters)


# character's inventory page route
@app.route("/character/inventory", methods=["GET"])
def get_character_inventory():
    return render_template("character_inventory.html", inventory=get_inventory(request.args.get('charID')),
                           equippedItem=get_equipped(request.args.get('charID'))[0],
                           character=get_char(request.args.get('charID'))[0])


# equip an item
@app.route("/character/inventory/equip", methods=["POST"])
def equip_item():
    data = request.form
    equip(data["charID"], data["itemID"])
    return redirect(url_for("get_character_inventory") + "?charID=" + data["charID"])


# unequip an item
@app.route("/character/inventory/unequip", methods=["POST"])
def unequip_item():
    data = request.form
    unequip(data["charID"])
    return redirect(url_for("get_character_inventory") + "?charID=" + data["charID"])


# redirect to store
@app.route("/redirect/store", methods=["POST"])
def redirect_store():
    data = request.form
    return redirect(url_for("enter_store") + "?charID=" + data["charID"])


# redirect to characterinfo
@app.route("/redirect/characterinfo", methods=["POST"])
def redirect_character_inventory():
    data = request.form
    return redirect(url_for("view_character_stats") + "?charID=" + data["charID"])


# redirect to character inventory
@app.route("/redirect/character/inventory", methods=["POST"])
def redirect_characterinfo():
    data = request.form
    return redirect(url_for("get_character_inventory") + "?charID=" + data["charID"])


# item store
@app.route("/character/inventory/store", methods=["GET"])
def enter_store():
    return render_template("item_shop.html", shop=get_all_items(), character=get_char(request.args.get('charID'))[0],
                           characterPurse=get_purse(request.args.get('charID'))[0][0])


# purchase an item
@app.route("/character/inventory/store/purchase", methods=["POST"])
def purchase_item():
    data = request.form
    purchase_items(data["charID"], data["itemID"], data["cost"])
    return redirect(url_for("get_character_inventory") + "?charID=" + data["charID"])


# sell an item
@app.route("/character/inventory/sell", methods=["POST"])
def sell_item():
    data = request.form
    sell_items(data["charID"], data["itemID"], data["cost"])
    unequip(data["charID"])
    return redirect(url_for("get_character_inventory") + "?charID=" + data["charID"])


# EXAMPLE OF POST REQUEST
@app.route("/new-character", methods=["POST"])
def create_char():
    try:
        # Get items from the form
        data = request.form
        char_first_name = data["firstname"]  # This is defined in the input element of the HTML form on index.html
        char_last_name = data["lastname"]
        char_beefiness = data["beefiness"]  # This is defined in the input element of the HTML form on index.html
        char_buffness = data["buffness"]
        char_smartness = data["smartness"]
        char_speediness = data["speediness"]
        user_id = session.get("user_id")
        class_id = data["class"]
        race_id = data["race"]

        insert_char(char_first_name, char_last_name, char_beefiness, char_buffness, char_smartness, char_speediness,
                    user_id, class_id, race_id)

        # Send message to page. There is code in index.html that checks for these messages
        flash("Character added successfully", "success")
        # Redirect to home. This works because the home route is named home in this file
        return redirect(url_for("add_character"))

    # If an error occurs, this code block will be called
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")  # Send the error message to the web page
        return redirect(url_for("add_character"))  # Redirect to home


# ------------------------ END ROUTES ------------------------ #


# listen on port 8080
if __name__ == "__main__":
    app.run(port=8080, debug=True)  # TODO: Students PLEASE remove debug=True when you deploy this for production!!!!!
