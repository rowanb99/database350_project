import os
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the flask app
app = Flask(__name__)
app.secret_key = os.getenv("SECRET")


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
    query = "SELECT ItemName, ItemCost, ItemBaseDamage, ItemBeefynessBonus,ItemSmartnessBonus, ItemSpeedinessBonus FROM item"
    cursor.execute(query)
    # Get result and close
    result = cursor.fetchall()  # Gets result from query
    conn.close()  # Close the db connection
    # (NOTE: You should do this after each query, otherwise your database may become locked)
    return result

def get_all_chars():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT CharacterFName, CharacterLName, CharacterBeefyness, CharacterBuffness, CharacterSmartness, CharacterSpeediness FROM characters"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result
def insertChar(firstname, lastname, beefiness, buffness, smartness, speediness):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO characters (CharacterFName, CharacterLName, CharacterBeefyness, CharacterBuffness, CharacterSmartness, CharacterSpeediness) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (firstname, lastname, beefiness, buffness, smartness, speediness))
    conn.commit()
    cursor.close()
    conn.close()
    
def getChar(characterID):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM CharacterInfo WHERE CharacterID=%s"
    cursor.execute(query, (characterID,))
    result = cursor.fetchall()
    conn.close()
    return result
    
def getInventory(characterID):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM Inventory WHERE CharacterID=%s"
    cursor.execute(query, (characterID,))
    result = cursor.fetchall()
    conn.close()
    return result

def getEquipped(characterID):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT EquippedItemID FROM characters WHERE CharacterID=%s"
    cursor.execute(query, (characterID,))
    result = cursor.fetchall()
    conn.close()
    return result

def equip(characterID, itemID):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE characters SET EquippedItemID=%s WHERE CharacterID=%s"
    cursor.execute(query, (itemID, characterID))
    conn.commit()
    cursor.close()
    conn.close()
    
def unequip(characterID):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE characters SET EquippedItemID=NULL WHERE CharacterID=%s"
    cursor.execute(query, (characterID,))
    conn.commit()
    cursor.close()
    conn.close()


# ------------------------ END FUNCTIONS ------------------------ #


# ------------------------ BEGIN ROUTES ------------------------ #
# EXAMPLE OF GET REQUEST
@app.route("/", methods=["GET"])
def home():
    items = get_all_items()  # Call defined function to get all items
    chars = get_all_chars()
    return render_template("index.html", items=items, chars=chars) #return the page to be rendered

# character list route
@app.route("/characters", methods=["GET"])
def view_all_characters():
    # Retrieve all characters from the database
    all_characters = get_all_chars()
    return render_template("character.html", all_characters=all_characters)

#character's inventory page route
@app.route("/character/inventory", methods=["GET"])
def get_character_inventory():
    return render_template("character_inventory.html", inventory=getInventory(request.args.get('charID')), equippedItem=getEquipped(request.args.get('charID'))[0], character=getChar(request.args.get('charID'))[0])
    
#equip an item
@app.route("/character/inventory/equip", methods=["POST"])
def equip_item(): 
    data = request.form
    equip(data["charID"], data["itemID"])
    return redirect(url_for("get_character_inventory") + "?charID=" + data["charID"])

#unequip an item
@app.route("/character/inventory/unequip", methods=["POST"])
def unequip_item(): 
    data = request.form
    unequip(data["charID"])
    return redirect(url_for("get_character_inventory") + "?charID=" + data["charID"])
    

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

        insertChar(char_first_name, char_last_name, char_beefiness, char_buffness, char_smartness, char_speediness)



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
