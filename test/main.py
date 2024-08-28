from os import getenv
from dotenv import load_dotenv


load_dotenv()
user = getenv('DB_USER')
password = getenv('DB_PASSWORD')
print(user, password)