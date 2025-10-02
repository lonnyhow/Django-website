from django.contrib import admin

from .models import Category, FAQ, Article, Comment, ArticleImage


class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 1


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'views', 'is_active', 'category', 'created_at']
    list_editable = ['is_active', 'category']
    list_filter = ['is_active', 'category', 'created_at']
    search_fields = ['title']
    readonly_fields = ['views']
    inlines = [ArticleImageInline]


admin.site.register(Category)  # добавляем нашу модель в админку
admin.site.register(FAQ)
admin.site.register(Comment)
admin.site.register(Article, ArticleAdmin)

# python manage.py createsuperuser
