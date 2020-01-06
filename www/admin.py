from django.contrib import admin
from .models import File, Author, Tag, Course

# Register your models here.
#admin.site.register(File)
#admin.site.register(Author)
#admin.site.register(Tag)
#admin.site.register(Course)


# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    pass
# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)


# Register the Admin classes for File using the decorator
@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_course',)
    list_filter = ('course',)

# Register the Admin classes for Course using the decorator
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass
