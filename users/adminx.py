# encoding: utf-8
# __author__ = 'mtianyan'
# __date__ = '2018/2/14 0014 01:17'


import xadmin
from xadmin import views
from .models import EmailVerifyRecord


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "宠物商城"
    site_footer = "vueshop@mtianyan.cn"
    # menu_style = "accordion"


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', "send_time"]


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
