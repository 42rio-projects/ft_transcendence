from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
import user.models as models


class IsFriendsWithInline(admin.TabularInline):
    model = models.IsFriendsWith
    fk_name = 'user1'


class IsBlockedByInline(admin.TabularInline):
    model = models.IsBlockedBy
    fk_name = 'blocker'


class UserAdm(UserAdmin):
    inlines = [IsFriendsWithInline, IsBlockedByInline]


admin.site.register(models.User, UserAdm)
admin.site.register(models.IsFriendsWith)
admin.site.register(models.IsBlockedBy)
