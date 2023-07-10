from django.contrib import admin

from events.models import (
    Event, EventImage, EventGalleryImage, Section, Ticket, Category, Organizer, Venue
)
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

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
    list_display = ('name', 'country', 'slug')


class VenueAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}
    list_display = ('name', 'country', 'slug')


class EventImageInline(admin.StackedInline):
    model = EventImage
    ordering = ("order",)
    extra = 0
    readonly_fields = ('image_width', 'image_height')


class EventGalleryImageInline(admin.StackedInline):
    model = EventGalleryImage
    extra = 0
    ordering = ("order",)
    readonly_fields = ('image_width', 'image_height')


class SectionInline(admin.StackedInline):
    model = Section
    extra = 0


class TicketInline(admin.StackedInline):
    model = Ticket
    extra = 0


class EventAdmin(admin.ModelAdmin,DynamicArrayMixin):
    inlines = [EventImageInline, EventGalleryImageInline, SectionInline, TicketInline]
    prepopulated_fields = {'slug': ('title', )}
    list_display = ('title', 'date', 'country', 'identifier', 'highlighted')
    list_filter = ('country', 'date', 'highlighted')
    search_fields = ('title', )
    fields = (
        'country', 'title', 'slug', 'category','organizer', 'date', 'date_text', 'pay_date', 'venue', 'online_event',
        'highlighted', 'published', 'main_image', 'main_image_width', 'main_image_height', 'individual_percentage'
    )
    readonly_fields = ('main_image_width', 'main_image_height')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Organizer, OrganizerAdmin)
admin.site.register(Venue, VenueAdmin)
