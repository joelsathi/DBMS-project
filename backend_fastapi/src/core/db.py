import mysql.connector
from mysql.connector.pooling import PooledMySQLConnection

from ..settings import settings

connection_pool: PooledMySQLConnection = mysql.connector.pooling.MySQLConnectionPool(
    use_pure=False,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    database=settings.DB_NAME,
    pool_size=settings.DB_POOL_SIZE,
)
