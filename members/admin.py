from django.contrib import admin
from members.models import Template, Template_Event

class TemplateAdmin(admin.ModelAdmin):
    list_display = ('male_name', 'female_name', 'date')

admin.site.register(Template, TemplateAdmin)

# Register your models here.
