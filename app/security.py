from app.models import *
from app.forms import *
from flask_social import Social
from flask_security import Security
from flask_security import SQLAlchemyUserDatastore
from flask_social.datastore import SQLAlchemyConnectionDatastore

######## Flask-security ###########
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(
    app, 
    user_datastore, 
    register_form=ExtendedRegisterForm,
    confirm_register_form=ExtendedConfirmRegisterForm,
    login_form=ExtendedLoginForm,
    )

social = Social(app, SQLAlchemyConnectionDatastore(db, Connection))

# Create all database tables
db.create_all()