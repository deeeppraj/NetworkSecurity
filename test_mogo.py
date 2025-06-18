
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from netwoksecurity.exception.exception import CustomException
import sys

uri = "mongodb+srv://workdeepraj:2FEcVBV37F1cTo6V@cluster0.hzts1zg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    raise CustomException(e,sys)