import json

from peewee import OperationalError
from peewee import Model, DatabaseProxy, SqliteDatabase, PostgresqlDatabase, SQL
from peewee import Field, AutoField, CharField, TextField, IntegerField, BooleanField, ForeignKeyField

database_proxy = DatabaseProxy()


def json_float_parser(string: str) -> float:
    """Функция парсинга типа float в json при десериализации.
    Необходима для избавления от экспоненты при десириализации, которая автоматически
    добавляется библиотекой json.

    :param string: строка с float.

    :return: отформатированный float без экспоненты.
    """
    format_s = '{:20.20}'.format(string)
    float_format_s = float(format_s)
    return float_format_s


class IvDBModel(Model):
    class Meta:
        database = database_proxy


class SettingMapper(IvDBModel):
    setid = AutoField()
    settypeid = IntegerField(null=False)
    setname = TextField(null=False)
    setvalue = TextField(null=False)
    setcomment = TextField(null=False)
    setinfo = TextField(null=False)
    sethash = TextField(null=False)

    class Meta:
        db_table = "setting"

    @staticmethod
    def get_free_id54() -> int:
        setting_mappers = SettingMapper.\
            select(SettingMapper.setvalue).\
            where(SettingMapper.settypeid == 1)

        id54_list = []
        for mapper in setting_mappers:
            setvalue = mapper.setvalue.replace("\\/", "\\\\/")
            setvalue_json = json.loads(setvalue, parse_float=json_float_parser)
            id54_list.append(setvalue_json['network_5_4'][0]['iv54server']['ID_54']["_value"])

        free_id54 = 1
        while True:
            if id54_list.count(free_id54) > 0:
                free_id54 += 1
                continue
            return free_id54
