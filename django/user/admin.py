from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import User, IsFriendsWith


class IsFriendsWithInline(admin.TabularInline):
    model = IsFriendsWith
    fk_name = 'user1'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user1=request.user)


class UserAdm(UserAdmin):
    inlines = [IsFriendsWithInline]


admin.site.register(User, UserAdm)
admin.site.register(IsFriendsWith)
