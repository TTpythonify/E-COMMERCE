##########################################################################
############################ MAIN.PY #####################################
##########################################################################


from flask import Flask
from BLUEPRINTS.login import login_bp
from BLUEPRINTS.signup import signup_bp
from BLUEPRINTS.home import home_bp

# BLUEPRINTS
app = Flask(__name__)
app.register_blueprint(login_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(home_bp)
app.config['SECRET_KEY'] = 'f3cfe9ed8fae309f02079dbf'

if __name__ == "__main__":
    app.run(debug=True)
