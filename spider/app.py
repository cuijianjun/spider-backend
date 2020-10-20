from flask import Flask
from spider.config import config
from spider.api import xyz_bp
from spider.util.orm_util import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.MYSQL_URL
app.register_blueprint(xyz_bp)
db.init_app(app)
