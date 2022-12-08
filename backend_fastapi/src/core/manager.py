from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor


class BaseManager:
    connection: MySQLConnection = None

    def __init__(self, model_class):
        self.model_class = model_class

    @classmethod
    def set_connection(cls, connection: MySQLConnection):
        cls.connection = connection

    @classmethod
    def _get_cursor(cls, dictionary=False) -> MySQLCursor:
        return cls.connection.cursor(dictionary=dictionary)

    def select(self, *field_names):
        # TODO validate?

        field_str = "*"
        if len(field_names) > 0:
            field_str = ",".join(field_names)

        sql_query_str = "SELECT {} FROM {}".format(
            field_str, self.model_class.__tablename__
        )

        cursor = self._get_cursor(dictionary=True)
        cursor.execute(sql_query_str)
        rows = cursor.fetchall()

        # TODO convert to objects? if needed only? have a separate method for that?

        return rows
