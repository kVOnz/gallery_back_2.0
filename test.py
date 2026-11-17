import os
from app.config import settings

print("файлы в папке:", os.listdir('.'))

from dotenv import load_dotenv
load_dotenv()

print("DB_URL from env:",os.getenv("DATABASE_URL"))
print("secret_key from env:",os.getenv("SECRET_KEY"))
print("тип объекта:", type(settings))
print("значение DATABASE_URL:", settings.DATABASE_URL)