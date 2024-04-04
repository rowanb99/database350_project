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
    cursor = conn.cursor()  # Creates a cursor for the connection, you need this to do queries
    # Query the db
    query = ("SELECT ItemName, ItemCost, ItemBaseDamage, ItemBeefynessBonus,ItemSmartnessBonus, ItemSpeedinessBonus "
             "FROM item")
    cursor.execute(query)
    # Get result and close
    result = cursor.fetchall()  # Gets result from query
    conn.close()  # Close the db connection
    # (NOTE: You should do this after each query, otherwise your database may become locked)
    return result


def get_all_chars():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = ("SELECT CharacterFName, CharacterLName, CharacterBeefyness, CharacterBuffness, CharacterSmartness, "
             "CharacterSpeediness FROM characters")
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result


def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT Username, UserPassword, UserEmail FROM user"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result


def insert_user(firstname, lastname, username, email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    query = "INSERT INTO user (UserFName, UserLName, UserEmail, UserPassword, Username) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (firstname, lastname, email, hashed_password, username))
    conn.commit()
    cursor.close()
    conn.close()


def insert_char(firstname, lastname, beefiness, buffness, smartness, speediness):
    conn = get_db_connection()
    cursor = conn.cursor()
    # TODO Fix this so you include default values (foreign keys)
    query = ("INSERT INTO characters (CharacterFName, CharacterLName, CharacterBeefyness, CharacterBuffness, "
             "CharacterSmartness, CharacterSpeediness) VALUES (%s, %s, %s, %s, %s, %s)")
    cursor.execute(query, (firstname, lastname, beefiness, buffness, smartness, speediness))
    conn.commit()
    cursor.close()
    conn.close()


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


def get_character(character_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = ("SELECT CharacterFName, CharacterLName, CharacterBeefyness, CharacterBuffness, "
             "CharacterSmartness, CharacterSpeediness FROM characters WHERE CharacterID = %s")
    cursor.execute(query, character_id)
    result = cursor.fetchone()
    conn.close()
    return result


def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)


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


# ------------------------ END FUNCTIONS ------------------------ #


# ------------------------ BEGIN ROUTES ------------------------ #
# EXAMPLE OF GET REQUEST
@app.route("/", methods=["GET"])
def home():
    if not session.get("logged_in"):
        return render_template("login.html")
    else:
        return render_template("index.html")  # return the page to be rendered


@app.route("/login", methods=["POST"])
def login():

    data = request.form
    username = data["username"]
    password = data["password"]

    right_password = verify_login(username, password)
    if right_password:
        session["logged_in"] = True
        session["username"] = username
        flash("Login successful", "success")
        return redirect(url_for("home"))
    else:
        flash("Invalid username or password", "error")
        return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    session["logged_in"] = False
    session.pop("username", None)
    flash("Logged out successfully", "success")
    return redirect(url_for("home"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            data = request.form
            firstname = data["firstname"]
            lastname = data["lastname"]
            username = data["username"]
            email = data["email"]
            password = data["password"]

            users = get_all_users()

            existing_users = [user[0] for user in users]
            if username in existing_users:
                flash("Username already exists. Please choose a different one.", "warning")
                return render_template("register.html")

            existing_email = [user[2] for user in users]
            if email in existing_email:
                flash("Email already exists. Please choose a different one.", "warning")
                return render_template("register.html")

            insert_user(firstname, lastname, username, email, password)
            session["logged_in"] = True
            session["username"] = username

            flash("Registration successful. You have been automatically logged in.", "success")
            return redirect(url_for("home"))

        except Exception as e:
            flash(f"An error occurred during registration: {str(e)}", "error")
            return redirect(url_for("register"))
    else:
        return render_template("register.html")


# character list route
@app.route("/characters", methods=["GET"])
def view_all_characters():
    # Retrieve all characters from the database
    all_characters = get_all_chars()
    return render_template("character.html", all_characters=all_characters)


# EXAMPLE OF POST REQUEST
@app.route("/new-item", methods=["POST"])
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

        insert_char(char_first_name, char_last_name, char_beefiness, char_buffness, char_smartness, char_speediness)

        # TODO: Insert this data into the database

        # Send message to page. There is code in index.html that checks for these messages
        flash("Item added successfully", "success")
        # Redirect to home. This works because the home route is named home in this file
        return redirect(url_for("home"))

    # If an error occurs, this code block will be called
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")  # Send the error message to the web page
        return redirect(url_for("home"))  # Redirect to home


# ------------------------ END ROUTES ------------------------ #


# listen on port 8080
if __name__ == "__main__":
    app.run(port=8080, debug=True)  # TODO: Students PLEASE remove debug=True when you deploy this for production!!!!!
