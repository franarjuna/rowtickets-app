from django.contrib import admin

from events.models import (
    Event, EventImage, EventGalleryImage, Category, Organizer, Venue
)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    fields = ('country', 'name', 'slug')
    list_display = ('name', 'slug', 'country')


class OrganizerAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


class VenueAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


class EventImageInline(admin.StackedInline):
    model = EventImage


class EventGalleryImageInline(admin.StackedInline):
    model = EventGalleryImage


class EventAdmin(admin.ModelAdmin):
    inlines = [EventImageInline, EventGalleryImageInline]
    prepopulated_fields = {'slug': ('title', )}
    list_display = ('title', 'date', 'country', 'identifier', )
    list_filter = ('country', 'date')
    search_fields = ('title', )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Organizer, OrganizerAdmin)
admin.site.register(Venue, VenueAdmin)
