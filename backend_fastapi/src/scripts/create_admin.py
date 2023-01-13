from ..auth.utils import get_password_hash
from ..auth.models import RegisteredUserDBModel, UserDBModel
from ..core.db import connection_pool
from ..core.manager import BaseQueryManager

if __name__ == "__main__":
    BaseQueryManager.set_connection_pool(connection_pool)

    registered_user = RegisteredUserDBModel(
        username="admin",
        password=get_password_hash("fooadmin"),
        firstname="admin",
        lastname="user",
        email="admin@sample.com",
        mobile_no="0112729729",
        is_admin=True,
    )
    registered_user.save()
    user = UserDBModel(is_guest=False, registered_user=registered_user)
    user.save()
