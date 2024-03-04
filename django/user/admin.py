from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import User, IsFriendsWith


class IsFriendsWithInline(admin.TabularInline):
    model = IsFriendsWith
    fk_name = 'user1'


class UserAdm(UserAdmin):
    inlines = [IsFriendsWithInline]


admin.site.register(User, UserAdm)
