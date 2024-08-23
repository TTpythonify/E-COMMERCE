##########################################################################
############################ LOGIN.PY ####################################
##########################################################################


from flask import Blueprint, render_template, request, session, url_for, redirect
from database.database import *
import bcrypt

login_bp = Blueprint("login_bp", __name__)

# Create the user table imported from the database file
create_table()

@login_bp.route('/', methods=['GET', 'POST'])
def login_route():
    error_message = ""
    if request.method == 'POST':
        name = request.form.get("username")
        password = request.form.get("password")
        
        # Retrieve the user's hashed password from the database
        hashed_password = get_user_password(name)

        if hashed_password:
            # Convert memoryview to bytes
            hashed_password_bytes = bytes(hashed_password)
            
            if bcrypt.checkpw(password.encode(), hashed_password_bytes):
                # STORING CURRENT USER USING SESSION
                session['username'] = name
                return redirect(url_for("home_bp.home_route"))  # Go to the "home_bp" and finds that function
            else:
                error_message = "Invalid username or password. Please try again."
        else:
            error_message = "Invalid username or password. Please try again."

    return render_template("login.html", error_message=error_message)
