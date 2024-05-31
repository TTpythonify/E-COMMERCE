"""
THIS IS THE BACKEND FILE
Imports and makes use of database functions.
USES API's to make requests
"""

from flask import Blueprint,render_template,session,request,jsonify
import requests
from database.database import *


home_bp = Blueprint("home_bp",__name__,url_prefix="/home")

# Create the tables in the database
create_table()

@home_bp.route('/', methods=['GET', 'POST'])
def home_route():
    message,total_results = "",""
    
    if request.method == "POST":
        # Get item_name and country
        item_name = request.form.get('item_name')
        country = request.form.get('country')

        total_results = find_item(item_name, country)
        print(total_results)  # For debugging purposes
        
        #  If total_results was empty (i.e., if product is not available)
        if not total_results:
            message = "Item Not Available!"

    # Store username in SESSION
    name = session.get("username")
    return render_template("home.html", name=name, total_results=total_results, message=message)


# Route for the user's favorite
@home_bp.route('/add_to_favorite', methods=['POST'])
def add_to_favorite():

    product_data = request.json
    action = product_data.get('action')
    user_name=session.get("username")

    #Get user_id 
    user_id=get_user_id(user_name)
    product_asin =product_data.get('product_asin',"Asin Not Available")

    # If like button is pressed
    if action == 'like':
        add_to_like_table(user_id,product_data)
        message = "Product added to favorites"

    # User wants to remove from liked
    elif action == 'unlike':
        print("Removed it from your favorites")
        remove_from_like_table(user_id,product_asin)
        message = "Product removed from favorites"

    return jsonify({"message": message}), 200


# Route to display uses liked products
@home_bp.route('/liked_products',methods=['GET','POST'])
def favorite_products():
    liked_products=""

    user_name=session.get("username")
    #Get user_id 
    user_id=get_user_id(user_name)
    liked_products=get_user_liked_products(user_id)

    for product_list in liked_products:
        print(f"{product_list[0]}\n")

    return render_template("liked_products.html",liked_products=liked_products)


# Finds the product based on users prompts
def find_item(item_name, country):
    try:

        url = "https://real-time-amazon-data.p.rapidapi.com/search"
        querystring = {"query": item_name, "page": "1", "country": country}
        headers = {
            "X-RapidAPI-Key": "1ae4654528msh82cf9d56f299a41p175eb1jsnebd34a46be13",
            "X-RapidAPI-Host": "real-time-amazon-data.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        response = response.json()

        # If item is not available
        if not response:
            return False

        else:
            # Get necessary information
            data = response.get("data")
            products = data.get("products")
            total_products_available = {
                "total_products": data.get("total_products", "Not Available"),
                "product": []
            }
            # Store them in a dictionary
            for item in products:
                """
                API documentation @ rapidapi.com
                """
                items_products = {
                    "asin":item.get("asin","Not Available"),
                    "product_title": item.get("product_title", "Not Available"),
                    "product_price": item.get("product_price", "Not Available"),
                    "product_star_rating": item.get("product_star_rating", "Not Available"),
                    "product_url": item.get("product_url", "Not Available"),
                    "product_photo": item.get("product_photo", "Not Available"),
                    "delivery": item.get("delivery", "Not Available")
                }

                total_products_available["product"].append(items_products)

            return total_products_available

    except Exception as e:
        return False
    

