from django.contrib import admin

from events.models import (
    Event, EventImage, EventGalleryImage, EventPlaces, EventTickets, Category, Organizer, Venue
)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    fields = (
        'country', 'name', 'slug', 'color', 'header_image',
        'header_image_width', 'header_image_height', 'order',
    )
    list_display = ('name', 'slug', 'country', 'published', 'order', 'color')
    readonly_fields = ('header_image_width', 'header_image_height')


class OrganizerAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    fields = ('country', 'name', 'slug', 'twitter_handle')


class VenueAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


class EventImageInline(admin.StackedInline):
    model = EventImage
    extra = 0
    readonly_fields = ('image_width', 'image_height')


class EventGalleryImageInline(admin.StackedInline):
    model = EventGalleryImage
    extra = 0
    readonly_fields = ('image_width', 'image_height')

class EventPlacesInline(admin.StackedInline):
    model = EventPlaces
    extra = 0
    readonly_fields = ('title', 'color')


class EventTicketsInline(admin.StackedInline):
    model = EventTickets
    extra = 0
    readonly_fields = ('user', 'price','cost')


class EventAdmin(admin.ModelAdmin):
    inlines = [EventImageInline, EventGalleryImageInline, EventPlacesInline, EventTicketsInline]
    prepopulated_fields = {'slug': ('title', )}
    list_display = ('title', 'date', 'country', 'identifier', 'highlighted')
    list_filter = ('country', 'date', 'highlighted')
    search_fields = ('title', )
    fields = (
        'title', 'slug', 'category', 'date', 'date_text', 'venue', 'online_event', 'highlighted',
        'published', 'main_image', 'main_image_width', 'main_image_height'
    )
    readonly_fields = ('main_image_width', 'main_image_height')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Organizer, OrganizerAdmin)
admin.site.register(Venue, VenueAdmin)
