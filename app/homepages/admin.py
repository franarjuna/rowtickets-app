from django.contrib import admin

from homepages.models import Homepage, HomepageSlide


class HomepageSlideInline(admin.StackedInline):
    extra = 0
    model = HomepageSlide
    readonly_fields = ('image_height', 'image_width')
    fields = (
        'date_text', 'venue_text', 'button_text', 'event', 'organizer', 'link',
        'image', 'image_width', 'image_height', 'order'
    )


class HomepageAdmin(admin.ModelAdmin):
    inlines = [HomepageSlideInline]


admin.site.register(Homepage, HomepageAdmin)
