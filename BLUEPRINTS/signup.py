##########################################################################
############################ SIGNUP.PY ###################################
##########################################################################


from flask import Blueprint, render_template,request
from database.database import *
import bcrypt

signup_bp= Blueprint("signup_bp",__name__,url_prefix="/signup")

@signup_bp.route('/',methods=['GET','POST'])
def signup_route():
    success_message = None
    error_message = None
    salt=bcrypt.gensalt()


    if request.method == 'POST':
        # Get the user's details
        name = request.form.get('username')
        password = request.form.get('password')

        hashed_password=bcrypt.hashpw(password.encode(), salt)

        try:
            insert_into_database(name, hashed_password)
            success_message = "Signup successful!."
        
        except psycopg2.errors.UniqueViolation:
            # If a unique constraint violation occurs (i.e., username already exists), inform the user
            error_message = "Username already exists. Please choose a different username."

        except Exception as e:
            error_message = "An error occurred. Please try again later."
            print(f"Error: {e}") # Debugging 
    return render_template('signup.html', success_message=success_message, error_message=error_message)

