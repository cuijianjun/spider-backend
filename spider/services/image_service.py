import hashlib
import time
from spider.orm.image import Image, db


class ImageService(object):

    @staticmethod
    def create(name, class_name, url, index):
        ima = Image(name=name, class_name=class_name,
                    url=url,
                    index=index,
                    hash_code=hashlib.md5(url.encode(encoding='UTF-8')).hexdigest())
        db.session.add(ima)
        db.session.commit()
        return ima

    @staticmethod
    def update_index(class_name, url, index):
        hash_code = hashlib.md5(url.encode(encoding='UTF-8')).hexdigest()
        ima = db.session.query(Image).filter(Image.class_name == class_name). \
            filter(Image.hash_code == hash_code).first()
        if ima:
            ima.index = index
            db.session.add(ima)
            db.session.commit()

    @staticmethod
    def check_url(class_name, url):
        hash_code = hashlib.md5(url.encode(encoding='UTF-8')).hexdigest()
        ima = db.session.query(Image).filter(Image.class_name == class_name).\
            filter(Image.hash_code == hash_code).first()
        if not ima:
            return True
        return False

    @staticmethod
    def delete_out_date_images():
        db.session.query(Image).filter(Image.create_time <= time.time() - 7 * 24 * 3600).\
            delete(synchronize_session=False)
        db.session.commit()
