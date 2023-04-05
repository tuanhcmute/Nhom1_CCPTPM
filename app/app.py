from app import createApp

# Create app
app = createApp()

# Register blueprints
from app.main import bp as mainBp
app.register_blueprint(mainBp)
from app.authen import bp as authenBp
app.register_blueprint(authenBp, url_prefix='/auth')
