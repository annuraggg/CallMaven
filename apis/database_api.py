import os
import pymongo
from dotenv import load_dotenv
load_dotenv()

print(os.getenv("MONGO_CLIENT"))
mongoclient = pymongo.MongoClient(os.getenv("MONGO_HOST"))
mongoDB = mongoclient[os.getenv("MONGO_CLIENT")]  # type: ignore

Users = mongoDB[os.getenv("MONGO_DB_USERS")]  # type: ignore
Cust = mongoDB[os.getenv("MONGO_DB_CUSTS")]  # type: ignore
Tickets = mongoDB[os.getenv("MONGO_DB_TICS")]  # type: ignore

Admin = mongoDB[os.getenv("MONGO_DB_ADMIN")]  # type: ignore
Calls = mongoDB[os.getenv("MONGO_DB_CALLS")]  # type: ignore
Categories = mongoDB[os.getenv("MONGO_DB_CATEGORIES")]  # type: ignore
