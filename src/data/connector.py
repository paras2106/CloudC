import certifi
from pymongo import MongoClient

from app.config import config as cfg


class Connection:
    HOST = None
    PORT = None
    USER_NAME = None
    PASSWORD = None
    DB_NAME = None
    CONNECTION = False
    _DB = None

    def __init__(self):
        self.HOST = cfg.get("mongo", "HOST")
        self.USER_NAME = cfg.get("mongo", "USER_NAME")
        self.PASSWORD = cfg.get("mongo", "PASSWORD")
        self.DB_NAME = cfg.get("mongo", "DB_NAME")
        self.HTTP = cfg.get("mongo", "HTTP")

    def get_db(self):
        if not self.CONNECTION:
            connection_url = f"{self.HTTP}://{self.USER_NAME}:{self.PASSWORD}@{self.HOST}/?authMechanism=DEFAULT"
            print(f"Connection Url: {connection_url}")
            client = MongoClient(connection_url, tlsCAFile=certifi.where())
            self._DB = client[self.DB_NAME]
            self.CONNECTION = True
        return self._DB

    def get_collections(self):
        qmul = self.get_db()
        qmul.list_collection_names()

    def get_jobs(self):
        qmul = self.get_db()
        data = qmul["jobs"]
        return data

    def push_jobs(self, jobs):
        qmul = self.get_db()
        collection = qmul["jobs"]
        collection.insert_many(jobs)
        return

    def get_user(self, email):
        qmul = self.get_db()
        collection = qmul["users"]
        res = collection.find_one(filter={"email": email})
        return res

    def save_user(self, email, first_name, last_name, attributes=None):
        if attributes is None:
            attributes = {}

        qmul = self.get_db()
        collection = qmul["users"]
        collection.insert_one(
            {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "attributes": attributes,
            }
        )
        return


mongo_db = Connection()
