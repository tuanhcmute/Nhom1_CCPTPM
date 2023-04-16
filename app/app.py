from app import createApp

# Create app
app = createApp()

# Register blueprints
from app.routes.main import bp as mainBp
app.register_blueprint(mainBp)

from app.routes.authen import bp as authenBp
app.register_blueprint(authenBp, url_prefix='/auth')

from app.routes.admin.usermanage import bp as usermanage
app.register_blueprint(usermanage, url_prefix='/admin/user-manage')
