from django.contrib import admin
from .models import Category, Tag, Image, CreateItem, UrlList, Post


class QuestionAdmin(admin.ModelAdmin):
    # list_display = ('complete')
    list_filter = [('upload_user__first_name'), 'category', 'brand']
    search_fields = ['upload_user', 'category', 'brand']

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Image)
admin.site.register(UrlList)
admin.site.register(CreateItem)

admin.site.register(Post)
