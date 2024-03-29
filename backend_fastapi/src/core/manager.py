from contextlib import contextmanager
from typing import Callable
from mysql.connector.pooling import PooledMySQLConnection, CMySQLConnection
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

        _all_fields = model_class.get_fields_by_name()

        obj = model_class(
            is_existing=True,
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

    connection_pool: PooledMySQLConnection = None

    def __init__(self, model_class):
        self.model_class = model_class

    @classmethod
    def set_connection_pool(cls, connection_pool: PooledMySQLConnection):
        cls.connection_pool = connection_pool

    @classmethod
    @contextmanager
    def _get_cursor(cls, cursor_class=CMySQLCursor) -> CMySQLCursor:
        connection: CMySQLConnection = cls.connection_pool.get_connection()
        cursor: CMySQLCursor = connection.cursor(cursor_class=cursor_class)
        try:
            yield cursor
            connection.commit()
        finally:
            cursor.close()
            connection.close()

    def _get_fields_by_name_str(self, field_names):
        _field_names = self.model_class.get_fields_by_name()

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

    def _get_where_clause(self, filters: dict):
        _field_names = self.model_class.get_fields_by_name()

        FILTER_CONDITIONS = {
            "": lambda param: " = %s",
            "gt": lambda param: " > %s",
            "gte": lambda param: " >= %s",
            "lt": lambda param: " < %s",
            "lte": lambda param: " <= %s",
            "in": lambda param: " IN ({})".format(
                ", ".join(["%s" for _ in range(len(param.split(",")))])
            ),
            "like": " LIKE %s",
        }

        # If there are no filters just return an empty string
        if len(filters) == 0:
            where_clause = ""
            filter_vals_list = []

        else:
            where_clause = ""
            filter_vals_list = []
            first_iter = True
            for field_name in filters.keys():
                # We will allow different conditions to be used as filters by allowing a suffix
                # appended to the actual field name with a "__" to determine said operation.
                # For eg: `id__gt=2` would be a greater than condition resulting in SQL that looks
                # like `id >= 2`.
                try:
                    stripped_field_name, suffix = field_name.split("__")
                except ValueError:
                    stripped_field_name = field_name
                    suffix = ""

                # Silently pass if the field name does not exist: we don't want to fail from a
                # filter, we would return an unfiltered queryset in that case
                if stripped_field_name in _field_names:
                    if not first_iter and where_clause[-4:] != "AND ":
                        where_clause += " AND "
                    else:
                        where_clause += "WHERE "
                    first_iter = False

                    filter_condition: Callable = FILTER_CONDITIONS[suffix]
                    where_clause += "{} {}".format(
                        stripped_field_name, filter_condition(filters[field_name])
                       )

                    if suffix == "in":
                        filter_vals = filters[field_name].split(",")
                        filter_vals_list.extend(filter_vals)
                    else:
                        filter_vals_list.append(filters[field_name])

        return where_clause, filter_vals_list

    def select(
        self,
        field_names: list = [],
        page_num: int = 1,
        page_size: int = 10,
        filters: dict = {},
        sort_keys: dict = {},
        get_row_count: bool = False,
    ):
        field_str = self._get_fields_by_name_str(field_names)

        start = (page_num - 1) * page_size

        if sort_keys is not None and len(sort_keys) > 0:
            sort_clause = "ORDER BY "
            for field, s_order in sort_keys.items():
                sort_clause += "{} {}".format(field, s_order)
                if field != list(sort_keys.keys())[-1]:
                    sort_clause += ","
            print(sort_clause)
        else:
            sort_clause = ""

        where_clause, filter_values_list = self._get_where_clause(filters)

        _count = None
        if get_row_count:
            _count = self._get_count(where_clause, filter_values_list)

        sql_query_str = "SELECT {} FROM {} {} {} LIMIT {} OFFSET {}".format(
            field_str,
            self.model_class.__tablename__,
            where_clause,
            sort_clause,
            page_size,
            start,
        )

        rows = []
        with self._get_cursor(MySQLModelCursor) as cursor:
            cursor.execute(sql_query_str, filter_values_list)
            cursor.set_model_class(self.model_class)
            rows = cursor.fetchall()

        return rows, _count

    def select_by_id(self, id: int, field_names: list = []):
        # We will have a specific method just for this since it will be an important application

        field_str = self._get_fields_by_name_str(field_names)

        sql_query_str = "SELECT {} FROM {} WHERE {}=%s".format(
            field_str,
            self.model_class.__tablename__,
            self.model_class.primary_key,
        )

        row = None
        with self._get_cursor(MySQLModelCursor) as cursor:
            cursor.execute(sql_query_str, (id,))
            cursor.set_model_class(self.model_class)
            row = cursor.fetchone()

        return row

    def _get_count(self, _filter_str, filter_values_list):
        sql_query_str = "SELECT COUNT(*) FROM {} {}".format(
            self.model_class.__tablename__, _filter_str
        )

        _count = None
        with self._get_cursor(CMySQLCursor) as cursor:
            cursor.execute(sql_query_str, filter_values_list)
            _count = cursor.fetchone()

        return _count[0]

    def _insert(self, field_dict: dict):
        """
        Insert a record into the database.

        NOTE: This should probably not be used directly, instead using the save method on a model
            which would in turn call this.
        """

        sql_query_str = "INSERT INTO {} ({}) VALUES ({})".format(
            self.model_class.__tablename__,
            ",".join(tuple(field_dict.keys())),
            ",".join(["%s" for f in field_dict.keys()]),
        )

        success = False
        row_id = None
        with self._get_cursor(CMySQLCursor) as cursor:
            cursor: CMySQLCursor
            cursor.execute(sql_query_str, tuple(field_dict.values()))
            if cursor.rowcount > 0:
                success = True
                row_id = cursor.lastrowid

        return success, row_id

    def _update(self, field_dict: dict, filter_dict: dict):
        """
        Update a record in the database.

        NOTE: This should probably not be used directly, instead using the save method on a model
            which would in turn call this.
        """

        sql_query_str = "UPDATE {} SET {} WHERE {}".format(
            self.model_class.__tablename__,
            ",".join(["{}=%s".format(fname) for fname in field_dict.keys()]),
            ",".join(["{}=%s".format(fname) for fname in filter_dict.keys()]),
        )

        success = False
        with self._get_cursor(CMySQLCursor) as cursor:
            cursor.execute(
                sql_query_str, tuple([*field_dict.values(), *filter_dict.values()])
            )
            if cursor.rowcount > 0:
                success = True

        return success

    def _delete(self, filter_dict: dict):
        """
        Delete a record in the database.

        NOTE: This should probably not be used directly, instead using the remove method on a model
            which would in turn call this.
        """

        sql_query_str = "DELETE FROM {} WHERE {}".format(
            self.model_class.__tablename__,
            ",".join(["{}=%s".format(fname) for fname in filter_dict.keys()]),
        )

        success = False
        with self._get_cursor(CMySQLCursor) as cursor:
            cursor.execute(sql_query_str, tuple(filter_dict.values()))
            if cursor.rowcount > 0:
                success = True

        return success
