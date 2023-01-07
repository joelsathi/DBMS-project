def get_pagination(path: str, total: int, serialized_rows: list=[], page_num: int = 1, page_size: int = 10):
    start = (page_num - 1) * page_size
    end = start + page_size

    ret = {
        "data": serialized_rows,
        "total": total,
        "count": page_size,
        "pagination": {}
    }

    if end >= total:
        ret["pagination"]["next"] = None

        if page_num > 1:
            ret["pagination"]["previous"] = f"{path}?page_num={page_num-1}&page_size={page_size}"
        else:
            ret["pagination"]["previous"] = None
    else:
        if page_num > 1:
            ret["pagination"]["previous"] = f"{path}?page_num={page_num-1}&page_size={page_size}"
        else:
            ret["pagination"]["previous"] = None

        ret["pagination"]["next"] = f"{path}?page_num={page_num+1}&page_size={page_size}"

    return ret