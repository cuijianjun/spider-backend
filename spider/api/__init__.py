from flask import Blueprint
from flask_restful import Api
from spider.util.imports import import_submodules


xyz_bp = Blueprint('api', __name__, url_prefix="/app")
xyz_api = Api(xyz_bp)

import_submodules(globals(), __name__, __path__)

