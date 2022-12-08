import mysql.connector
from mysql.connector import MySQLConnection

from ..settings import settings

connection: MySQLConnection = mysql.connector.connect(
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    database=settings.DB_NAME,
    pool_size=settings.DB_POOL_SIZE,
)
