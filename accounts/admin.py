from django.contrib import admin
from .models import CustomUser, Post_Inquiry, Certification, Skill, Reward
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class QuestionAdmin(admin.ModelAdmin):
    list_filter = ['complete', 'created']
    search_fields = ['title', 'first_name', 'last_name']

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name','last_name',  'is_active', 'is_staff')
    list_filter = (
        'is_active', 
        'is_staff'
    )
    ordering = ("email", 'is_active', 'is_staff')


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Post_Inquiry, QuestionAdmin)
admin.site.register(Certification)
admin.site.register(Skill)
admin.site.register(Reward)

