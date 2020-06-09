from app.models import *
#from app import view
from app.forms import *

######## Flask-security ###########
# app.config['SECURITY_REGISTERABLE'] = True # create a user registration endpoint
# app.config['SECURITY_RECOVERABLE'] = True # create a password reset/recover endpoint
# app.config['SECURITY_CONFIRMABLE'] = True # specifies if users are required to confirm their email address when registering a new account. 


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(
    app, 
    user_datastore, 
    register_form=ExtendedRegisterForm,
    confirm_register_form=ExtendedConfirmRegisterForm,
    )