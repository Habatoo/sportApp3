from app.models import *
from app.forms import *

######## Flask-security ###########
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(
    app, 
    user_datastore, 
    register_form=ExtendedRegisterForm,
    confirm_register_form=ExtendedConfirmRegisterForm,
    login_form=ExtendedLoginForm,
    )

# Create all database tables
db.create_all()