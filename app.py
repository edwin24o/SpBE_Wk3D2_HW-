from application import create_app
from application.models import db
from flask_limiter.util import get_remote_address
from flask_limiter import Limiter

app = create_app('DevelopmentConfig')

limiter = Limiter(get_remote_address, app=app, default_limits=["10 perday", "40 per hour"])

if __name__ == '__main__':

    with app.app_context():
        # db.drop_all()
        db.create_all()
        
        

    app.run(debug=True)


    