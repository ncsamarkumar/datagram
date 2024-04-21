import json
import logging
from configparser import ConfigParser
from json.decoder import JSONDecodeError
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tables import Base, Product  # Assuming tables.py contains the Base and Product definitions

class DataProcessor:
    """A class to process data from a JSON file and store it in a database."""

    def __init__(self, jsonfilename):
        """
        Initialize the DataProcessor instance.

        Parameters:
        - jsonfilename (str): The filename of the JSON file containing the data.
        """
        self.config = ConfigParser()
        self.config.read("config.ini")
        pwd = quote_plus(self.config["DATABASE"]["PWD"])
        self.json_file = jsonfilename
        self.db_config = {
            'host': self.config["DATABASE"]["HOST"],
            'user': self.config["DATABASE"]["USR"],
            'password': pwd,
            'database': self.config["DATABASE"]["DB"],
            'port':self.config["DATABASE"]["PORT"]
        }
        # Create the database engine and session
        self.engine = create_engine(
            f"mysql+mysqlconnector://{self.db_config['user']}:{self.db_config['password']}@{self.db_config['host']}:{self.db_config['port']}/{self.db_config['database']}"
        )
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.logger = self.setup_logger()

    def setup_logger(self):
        """
        Set up the logger for logging errors and information.
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler('data_processing.log')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    def read_json_data(self):
        """
        Read JSON data from the specified file.

        Returns:
        - data (list): A list containing the JSON data.
        """
        try:
            with open(self.json_file, 'r', encoding="utf-8") as file_:
                data = json.load(file_)
            return data
        except JSONDecodeError as jsonexcep:
            self.logger.error(f"Error reading JSON file: {jsonexcep}. The JSON file contains extra data.")
            return None
        except Exception as excep:
            self.logger.error(f"Error reading JSON file: {excep}")
            return None

    def write_to_database(self, data):
        """
        Write data to the database.

        Parameters:
        - data (list): A list containing the data to be written to the database.
        """
        try:
            session = self.Session()
            for item in data:
                product = Product(
                    name=item.get('name', ''),
                    brand=item.get('brand', ''),
                    productUrl=item.get('productUrl', ''),
                    price=item.get('price', ''),
                    imageUrl=item.get('imageUrl', ''),
                    timeStamp=item.get('timeStamp', '')
                )
                session.add(product)
            session.commit()
            self.logger.info("Data successfully inserted into the database.")
        except Exception as excep:
            self.logger.error(f"Error writing data to database: {excep}")
            session.rollback()
        finally:
            session.close()

    def main(self):
        """
        Main method to execute the data processing steps.
        """
        json_data = self.read_json_data()
        if json_data:
            self.write_to_database(json_data)
            print("Data written to database")

if __name__ == "__main__":
    dataprocess = DataProcessor("pascal_coste.json")
    dataprocess.main()
