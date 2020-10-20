from flask_script import Manager, Server
from flask_migrate import MigrateCommand, Migrate
from spider.app import app
from spider.orm import *
from index_splider.index import SpiderScript

manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command("runserver", Server())
manager.add_command("db", MigrateCommand)
manager.add_command("spider", SpiderScript)

if __name__ == '__main__':
    manager.run()
