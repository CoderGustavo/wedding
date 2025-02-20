from os import getenv
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from a .env file for security
load_dotenv()

class Connection:
    """
    MongoDB Connection class.
    This class initializes the connection parameters and provides a method to
    establish a connection to the MongoDB database.
 
    Methods:
        - __init__: Initializes connection parameters from environment variables.
        - get_connection: Establishes a connection and returns a database object.
    """
 
    def __init__(self):
        """
        Initializes connection parameters from environment variables to enhance security.
        Ensures sensitive information is not hard-coded into the source code.
        """
        self.mongo_uri = getenv("MONGO_URI", "mongodb://localhost:27017")
        self.db_name = getenv("MONGO_DB_NAME", "default_db")

    def get_connection(self):
        """
        Establishes a connection to the MongoDB database using the provided parameters.

        Returns:
            pymongo.database.Database: MongoDB database object to interact with the database.
        Raises:
            Exception: If a connection could not be established.
        """
        try:
            # Create a MongoClient instance
            client = MongoClient(self.mongo_uri)

            # Return the database object
            return client[self.db_name]
        except Exception as e:
            # Print error and raise an exception if connection fails
            print("Failed to connect to MongoDB:", e)
            raise Exception("MongoDB connection failed") from e
