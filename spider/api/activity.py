import hashlib
from time import time
from flask_restful import Resource
from spider.api import xyz_api
from spider.util.jwt_utils import jwt_decode, jwt_encode
from spider.orm.image import Image, db
from sqlalchemy import distinct, func
from spider.util.server_exception import ServerException
from flask_restful.reqparse import RequestParser
from spider.util.auth import uniform_verification


def check_jwt_token(data):
    try:
        dic = jwt_decode(data)
        if time() - dic["time"] > int(dic["expires"]):
            raise ServerException(3000)
    except:
        raise ServerException(3001)


@xyz_api.resource('/generate_code')
class ImageGenerateCode(Resource):
    get_parser = RequestParser()
    get_parser.add_argument('expires', type=int, default=24*60*60)

    @uniform_verification()
    def get(self):
        args = self.get_parser.parse_args()
        token = jwt_encode({
            "time": time(),
            "expires": args["expires"]
        })
        return {"token": token.decode()}


@xyz_api.resource('/class_list')
class ClassListApi(Resource):

    get_parser = RequestParser()
    get_parser.add_argument('token', required=True)
    get_parser.add_argument('page', type=int, default=1)
    get_parser.add_argument('limit', type=int, default=100)

    @uniform_verification()
    def get(self):
        args = self.get_parser.parse_args()
        check_jwt_token(args["token"])
        result = []
        class_list = db.session.query(distinct(Image.class_name)).all()
        numbers_map = db.session.execute(
            "select class_name, count(class_name) from image where create_time >= %s group by class_name" % int(
                time() - 7 * 24 * 3600)).fetchall()
        numbers_map = dict(numbers_map or [])
        for class_name in class_list:
            result.append({
                'name': class_name[0],
                'number': numbers_map.get(class_name[0], 0)
            })
        return result


@xyz_api.resource('/images')
class ImagesApi(Resource):
    get_parser = RequestParser()
    get_parser.add_argument('token', required=True)
    get_parser.add_argument('page', type=int, default=1)
    get_parser.add_argument('limit', type=int, default=20)
    get_parser.add_argument('class_name', required=True)

    @uniform_verification()
    def get(self):
        args = self.get_parser.parse_args()
        check_jwt_token(args["token"])
        page, limit = args["page"], args["limit"]
        images = db.session.query(Image).filter(Image.create_time >= time() - 7 * 24 * 60 * 60).\
            filter(Image.class_name == args["class_name"]).\
            order_by(Image.index, Image.create_time.desc()).slice((page-1)*limit, page*limit).all()
        result = []
        counts = db.session.query(func.count(Image.id)).filter(Image.create_time >= time() - 7 * 24 * 60 * 60).\
            filter(Image.class_name == args["class_name"]).first()
        for ima in images:
            result.append({
                "name": ima.name,
                "class_name": ima.class_name,
                "url": ima.url,
                "create_time": ima.create_time,
                "id": ima.id
            })
        return {
            "list": result,
            "count": counts[0]
        }


@xyz_api.resource('/image')
class ImageApi(Resource):

    post_parser = RequestParser()
    post_parser.add_argument('name', required=True)
    post_parser.add_argument('url', required=True)
    post_parser.add_argument('class_name', required=True)

    @uniform_verification()
    def post(self):
        args = self.post_parser.parse_args()
        ima = Image(name=args["name"], class_name=args["class_name"],
                    url=args["url"],
                    hash_code=hashlib.md5(args["url"].encode(encoding='UTF-8')).hexdigest())
        db.session.add(ima)
        db.session.commit()
        return {}


@xyz_api.resource('/class_list_forever')
class ImagesForeverApi(Resource):

    get_parser = RequestParser()
    get_parser.add_argument('page', type=int, default=1)
    get_parser.add_argument('limit', type=int, default=100)

    @uniform_verification()
    def get(self):
        result = []
        class_list = db.session.query(distinct(Image.class_name)).filter(Image.create_time >= int(time()) - 3600 * 7 * 24).all()
        numbers_map = db.session.execute(
            "select class_name, count(class_name) from image where create_time >= %s group by class_name" % int(time() - 7 * 24 * 3600)).fetchall()
        numbers_map = dict(numbers_map or [])
        for class_name in class_list:
            result.append({
                'name': class_name[0],
                'number': numbers_map.get(class_name[0], 0)
            })
        return result


@xyz_api.resource('/images_forever')
class ImagesApiForever(Resource):
    get_parser = RequestParser()
    get_parser.add_argument('page', type=int, default=1)
    get_parser.add_argument('limit', type=int, default=20)
    get_parser.add_argument('class_name', required=True)

    @uniform_verification()
    def get(self):
        args = self.get_parser.parse_args()
        page, limit = args["page"], args["limit"]
        images = db.session.query(Image).filter(Image.create_time >= time() - 7 * 24 * 60 * 60).\
            filter(Image.class_name == args["class_name"]).\
            order_by(Image.index, Image.create_time.desc()).slice((page-1)*limit, page*limit).all()
        result = []
        counts = db.session.query(func.count(Image.id)).filter(Image.create_time >= time() - 7 * 24 * 60 * 60). \
            filter(Image.class_name == args["class_name"]).first()
        for ima in images:
            result.append({
                "name": ima.name,
                "class_name": ima.class_name,
                "url": ima.url,
                "create_time": ima.create_time,
                "id": ima.id
            })
        return {
            "list": result,
            "count": counts[0] if counts else 0
        }
