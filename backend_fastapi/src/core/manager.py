from mysql.connector import CMySQLConnection
from mysql.connector.cursor_cext import CMySQLCursor


class InvalidFieldException(Exception):
    pass


class InvalidModelException(Exception):
    pass


class MySQLModelCursor(CMySQLCursor):
    _raw = False
    model_class = None

    def set_model_class(self, model_class):
        self.model_class = model_class

    def _row_to_python(self, row):
        """Convert tuple returned from query into python object of relevant class"""

        model_class = self.model_class
        if model_class is None:
            raise InvalidModelException(
                "No model named {} found. Check if you have correctly set a model".format(
                    model_class
                )
            )

        obj = model_class(
            **{
                column_name: model_class._fields[column_name].from_db(value)
                for (column_name, value) in zip(self.column_names, row)
            }
        )
        return obj

    def fetchone(self):
        """Return next row of a query result set.

        Returns:
            None or object: a row from the query result set converted into relevant python object.
        """

        row = super().fetchone()
        if row:
            return self._row_to_python(row)

        return None

    def fetchmany(self, size=1):
        """Return the next set of rows of a query result set.

        When no more rows are available, it returns an empty list.
        The number of rows returned can be specified using the size argument,
        which defaults to one.

        Returns:
            list: The next set of rows of a query result set.
        """
        res = super().fetchmany(size=size)
        return [self._row_to_python(row) for row in res]

    def fetchall(self):
        """Return all rows of a query result set.

        Returns:
            list: A list of objects with all rows of a query result set.
        """

        res = super().fetchall()
        return [self._row_to_python(row) for row in res]


class BaseQueryManager:
    """NOTE: Currently all the methods depend on using the python mysql connector"""

    connection: CMySQLConnection = None

    def __init__(self, model_class):
        self.model_class = model_class

    @classmethod
    def set_connection(cls, connection: CMySQLConnection):
        cls.connection = connection

    @classmethod
    def _get_cursor(cls) -> CMySQLCursor:
        return cls.connection.cursor(cursor_class=MySQLModelCursor)

    def select(self, field_names: list = [], filters: dict = None):
        # TODO implement filters (WHERE queries), limits, sorting (ORDER BY queries)

        # If field names are specified, select only those. Otherwise select all model fields.
        if len(field_names) == 0:
            field_names = list(self.model_class._fields.keys())

        field_str = ""
        for ind, field_name in enumerate(field_names):
            # Throw an exception if the field names are not valid
            if field_name not in self.model_class._fields:
                raise InvalidFieldException(
                    "No field named {} found on {}".format(
                        field_name, self.model_class.__qualname__
                    )
                )
            else:
                field_str += field_name
                if ind < len(field_names) - 1:
                    field_str += ","

        sql_query_str = "SELECT {} FROM {}".format(
            field_str, self.model_class.__tablename__
        )

        cursor: MySQLModelCursor = self._get_cursor()
        cursor.execute(sql_query_str)
        cursor.set_model_class(self.model_class)
        rows = cursor.fetchall()
        cursor.close()

        return rows
