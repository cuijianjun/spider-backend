from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Data(object):

    def __init__(self, name, value, desc=''):
        self.name = name
        self.value = value
        self.desc = desc

    def __eq__(self, other):
        if isinstance(other, Data):
            return self.value == other.value
        return self.value == other


class EmuObject(object):

    def __init__(self, tuple_info):
        self._data = {}
        self._value = {}
        for info in tuple_info:
            length = len(info)
            assert length >= 2
            d_obj = Data(*info)
            self._data[d_obj.name] = d_obj
            self._value[d_obj.value] = d_obj

    def __getattr__(self, item):
        return self._data[item].value

    def get_desc(self, item):
        return self._value[item].desc


def generate_sql_text(filter_dic):
    """
    Example:
        query.filter(text(sqltext)).params(**params)

    :param
        # Status是一个Enum类
        filter_dic: {
                        "table1.name": "xiaoming",
                        "table2.age": [12, 13],
                        "table1.status": Status.FINISH
                    }
    :return:
        返回值是一个元组，格式为(sqltext, params)
        (
            "table1.name = :table1_name and table2.age in :table2_age and table1.status = table1_status",
            {
                "table1_name": "xiaoming",
                "table2_age": [12, 13],
                "table1_status": 1
            }
        )
    """
    and_sql_text_list = []
    sql_params = {}
    for k, v in filter_dic.items():
        _k = k
        if "." in k:
            _k = "_".join(k.split("."))
        if v is None:
            continue
        elif type(v) in (tuple, list):
            and_sql_text_list.append(" %s in :%s" % (k, _k))
            sql_params[_k] = v
        else:
            and_sql_text_list.append(" %s = :%s " % (k, _k))
            # 很多时候v是Enum类的属性，需要获取其原始的值
            sql_params[_k] = getattr(v, "value", v)

    raw_sql = " and ".join(and_sql_text_list)
    return raw_sql, sql_params


def update_orm_obj(orm_obj, update_dic):

    for k, v in update_dic.items():
        if v is not None:
            setattr(orm_obj, k, v)


if __name__ == '__main__':

    e = EmuObject((('agree', 1, '参加'), ('refuse', 2, '拒绝')))
    print(e.agree, e.get_desc(e.agree))
