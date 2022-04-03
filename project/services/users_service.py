from flask import current_app
from project.dao import UserDAO
from project.exceptions import ItemNotFound
from project.schemas.user import UserSchema
from project.services.base import BaseService
from project.tools.security import generate_password_digest, compare_password


class UsersService(BaseService):
    def get_item_by_id(self, pk):
        user = UserDAO(self._db_session).get_by_id(pk)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def get_item_by_email(self, email):
        user = UserDAO(self._db_session).get_by_email(email)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def get_all_users(self):
        users = UserDAO(self._db_session).get_all()
        return UserSchema(many=True).dump(users)

    def get_limit_users(self, page):
        limit = current_app.config["ITEM_PER_PAGE"]
        offset = (page - 1) * limit
        users = UserDAO(self._db_session).get_limit(limit=limit, offset=offset)
        return UserSchema(many=True).dump(users)

    def create(self, data_in):
        user_pass = data_in.get("password")
        if user_pass:
            data_in["password"] = generate_password_digest(user_pass)
        user = UserDAO(self._db_session).create(data_in)
        return UserSchema().dump(user)

    def update(self, data_in):
        user = UserDAO(self._db_session).update(data_in)
        return UserSchema().dump(user)

    def update_pass(self, data_in, user_id):
        user_password_1 = data_in.get("password_1")
        user_password_2 = data_in.get("password_2")
        # user_id = data_in.get("id")
        user_password = UserDAO(self._db_session).get_by_id(user_id)
        if compare_password(user_password, user_password_1):
            user = UserDAO(self._db_session).update(data_in)
            return UserSchema().dump(user)






    # def get_filter_movies(self, filter_args):
    #     limit = 0
    #     offset = 0
    #     if filter_args.get("page"):
    #         limit = current_app.config["ITEMS_PER_PAGE"]
    #         offset = (filter_args.get("page") - 1) * limit
    #     status = filter_args.get("status")
    #     movies = UserDAO(self._db_session).get_filter(limit=limit, offset=offset, status=status)
    #     return UserSchema(many=True).dump(movies)
