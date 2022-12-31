from django.contrib import admin

from homepages.models import Homepage, HomepageSlide


class HomepageSlideInline(admin.StackedInline):
    extra = 0
    model = HomepageSlide


class HomepageAdmin(admin.ModelAdmin):
    inlines = [HomepageSlideInline]


admin.site.register(Homepage, HomepageAdmin)
