def get_pagination(
    path: str,
    total: int,
    serialized_rows: list = [],
    page_num: int = 1,
    page_size: int = 10,
):
    start = (page_num - 1) * page_size
    end = start + page_size

    ret = {
        "data": serialized_rows,
        "total": total,
        "count": page_size,
        "pagination": {},
    }

    if end >= total:
        ret["pagination"]["next"] = None

        if page_num > 1:
            ret["pagination"][
                "previous"
            ] = f"{path}?page_num={page_num-1}&page_size={page_size}"
        else:
            ret["pagination"]["previous"] = None
    else:
        if page_num > 1:
            ret["pagination"][
                "previous"
            ] = f"{path}?page_num={page_num-1}&page_size={page_size}"
        else:
            ret["pagination"]["previous"] = None

        ret["pagination"][
            "next"
        ] = f"{path}?page_num={page_num+1}&page_size={page_size}"

    return ret


def get_params(param_dict: dict):

    page_num = 1
    page_size = 10
    sort_by = []
    sort_orders = []
    where_params = dict()

    for key, val in param_dict.items():
        if key == "page_num":
            page_num = int(val)
        elif key == "page_size":
            page_size = int(val)
        elif key == "sort_by":
            sort_by = val.split(",")
        elif key == "sort_orders":
            sort_orders = val.split(",")
        else:
            where_params[key] = val.split(",")

    for key, val in where_params.items():
        temp = []
        for v in val:
            cur = '"' + v + '"'
            temp.append(cur)
        where_params[key] = temp

    if sort_by and sort_orders:
        sort_dict = dict(zip(sort_by, sort_orders))
    else:
        sort_dict = dict()

    return [page_num, page_size, sort_dict, where_params]
