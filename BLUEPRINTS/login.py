from flask import Blueprint, render_template,request,session,url_for,redirect
from database.database import *


login_bp= Blueprint("login_bp",__name__)

# Create the user table imported from the database file
create_table()


@login_bp.route('/',methods=['GET','POST'])
def login_route():
    error_message=""
    if request.method == 'POST':
        name= request.form.get("username")
        password=request.form.get("password")
        
        # Checking if the username is in the database
        details = username_in_database(name, password)

        if details:
            # STORING CURRENT USER USING SESSION
            session['username'] = name
            return redirect(url_for("home_bp.home_route"))# Go to the "home_bp" and finds that function
        else:
            error_message = "Invalid username or password. Please try again."

    return render_template("login.html",error_message=error_message)

