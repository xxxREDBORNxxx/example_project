import json
import hashlib
from peewee import SqliteDatabase

from test_utils.iv7.server.backend.sqlite import models


def connect(db_path):
    database = SqliteDatabase(db_path, pragmas={
        'journal_mode': 'wal'
    })
    models.database_proxy.initialize(database)
    return database


def disconnect(database):
    database.close()


def insert_graph_from_file(file_path: str, server: str, profile: str) -> tuple:
    with open(file_path, encoding='utf-8') as f:
        graph = json.load(f)

    free_id54 = models.SettingMapper.get_free_id54()
    key2 = f"py_test_{free_id54}"

    graph['network_5_4'][0]['iv54server']['ID_54']["_value"] = free_id54
    graph['common']['key2'] = key2

    setname = f"{server}_{key2}_{profile}"
    sethash = hashlib.md5(json.dumps(graph).encode('UTF-8')).hexdigest()
    setting = models.SettingMapper.create(
        settypeid=1,
        setname=setname,
        setvalue=json.dumps(graph).replace("\\\\/$", "\\/$"),
        setcomment="",
        setinfo="",
        sethash=sethash
    )
    return setting, key2
