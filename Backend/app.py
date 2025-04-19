from flask import Flask
from config import Config
from db import db, migrate

from Routes import routes  # Corrected import to match filename case and single blueprint

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)

app.register_blueprint(routes)  # Register the single blueprint

if __name__ == '__main__':
    app.run(debug=True)
