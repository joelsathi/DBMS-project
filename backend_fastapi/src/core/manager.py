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

        _all_fields = model_class.get_field_names()

        obj = model_class(
            **{
                column_name: _all_fields[column_name].from_db(value)
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

    def _get_field_names_str(self, field_names):
        _field_names = self.model_class.get_field_names()

        # If field names are specified, select only those. Otherwise select all model fields.
        if len(field_names) == 0:
            field_str = ",".join(_field_names.keys())

        else:
            field_str = ""
            for ind, field_name in enumerate(field_names):
                # Throw an exception if the field names are not valid
                if field_name not in _field_names:
                    raise InvalidFieldException(
                        "No field named {} found on {}".format(
                            field_name, self.model_class.__qualname__
                        )
                    )
                else:
                    field_str += field_name
                    if ind < len(field_names) - 1:
                        field_str += ","

        return field_str

    def select(self, field_names: list = [], filters: dict = None):
        # TODO implement filters (WHERE queries), limits, sorting (ORDER BY queries)

        field_str = self._get_field_names_str(field_names)

        sql_query_str = "SELECT {} FROM {}".format(
            field_str, self.model_class.__tablename__
        )

        cursor: MySQLModelCursor = self._get_cursor()
        cursor.execute(sql_query_str)
        cursor.set_model_class(self.model_class)
        rows = cursor.fetchall()
        cursor.close()

        return rows

    def select_by_id(self, id: int, field_names: list = []):
        # We will have a specific method just for this since it will be an important application

        field_str = self._get_field_names_str(field_names)

        sql_query_str = "SELECT {} FROM {} WHERE {}=%s".format(
            field_str,
            self.model_class.__tablename__,
            self.model_class.primary_key,
        )

        cursor: MySQLModelCursor = self._get_cursor()
        cursor.execute(sql_query_str, (id,))
        cursor.set_model_class(self.model_class)
        row = cursor.fetchone()
        cursor.close()

        return row
    
    # def get_count(self):

    #     sql_query_str = "SELECT COUNT(*) FROM {}".format(
    #         self.model_class.__tablename__
    #     )

    #     cursor: MySQLModelCursor = self._get_cursor()
    #     cursor.execute(sql_query_str)
    #     cursor.set_model_class(self.model_class)
    #     count = cursor.fetchone()
    #     print(count)
    #     cursor.close()

    #     return count
    
    def select_by_page(self, field_names: list = [], page_num: int = 1, page_size: int = 10, filters: dict = None):
        # TODO implement filters (WHERE queries), limits, sorting (ORDER BY queries)

        field_str = self._get_field_names_str(field_names)

        start = (page_num - 1)*page_size

        sql_query_str = "SELECT {} FROM {} LIMIT {} OFFSET {}".format(
            field_str, self.model_class.__tablename__, page_size, start
        )

        cursor: MySQLModelCursor = self._get_cursor()
        cursor.execute(sql_query_str)
        cursor.set_model_class(self.model_class)
        rows = cursor.fetchall()
        cursor.close()

        return rows

    def select_by_all(self, field_names: list = [], page_num: int = 1, page_size: int = 10, filters: dict = None, sort_ : dict = None):
        field_str = self._get_field_names_str(field_names)

        start = (page_num - 1)*page_size

        if sort_ is not None and len(sort_) > 0:
            sort_clause = "ORDER BY "
            temp = []
            for field, s_order in sort_.items():
                sort_clause += "{} {}".format(field, s_order) 
                if field != list(sort_.keys())[-1]:
                    sort_clause += ","
            print(sort_clause)
        else:
            sort_clause = ""

        # Check if any filters were provided
        if filters is not None and len(filters) > 0:
            # Build the WHERE clause based on the filters
            where_clause = "WHERE "
            for field, value in filters.items():
                # Add each filter condition to the clause
                where_clause += "{} = '{}'".format(field, value)
                # Add an AND operator after each condition except for the last one
                if field != list(filters.keys())[-1]:
                    where_clause += " AND "
        else:
            where_clause = ""

        sql_query_str = "SELECT {} FROM {} {} {} LIMIT {} OFFSET {}".format(
            field_str, self.model_class.__tablename__, where_clause, sort_clause, page_size, start
        )

        cursor: MySQLModelCursor = self._get_cursor()
        cursor.execute(sql_query_str)
        cursor.set_model_class(self.model_class)
        rows = cursor.fetchall()
        cursor.close()

        return rows
