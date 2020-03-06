import xadmin
from .models import UserFav, UserAddress


class UserFavAdmin(object):
    list_display = ['user', 'goods', "add_time"]


# class UserLeavingMessageAdmin(object):
#     list_display = ['user', 'message_type', "message", "add_time"]


class UserAddressAdmin(object):
    list_display = ["signer_mobile", "address"]

xadmin.site.register(UserFav, UserFavAdmin)
xadmin.site.register(UserAddress, UserAddressAdmin)
# xadmin.site.register(UserLeavingMessage, UserLeavingMessageAdmin)
