from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin as UnfoldModelAdmin

from address.models import Branch, City, Country, State
from common.admin import BaseAdmin


@admin.register(Country)
class CountryAdmin(BaseAdmin):
    list_display = ["label", "created_at", "updated_at"]
    list_filter = ["is_active"]
    search_fields = ["label"]
    ordering = ["label"]
    readonly_fields = ["id", "created_at", "updated_at", "_is_deleted", "_deleted_at"]


@admin.register(State)
class StateAdmin(BaseAdmin):
    list_display = ["label", "country", "created_at", "updated_at"]
    list_filter = ["country", "is_active"]
    search_fields = ["label", "country__label"]
    ordering = ["country__label", "label"]
    readonly_fields = ["id", "created_at", "updated_at", "_is_deleted", "_deleted_at"]


@admin.register(City)
class CityAdmin(BaseAdmin):
    list_display = ["label", "state", "created_at", "updated_at"]
    list_filter = ["state", "state__country", "is_active"]
    search_fields = ["label", "state__label", "state__country__label"]
    ordering = ["state__country__label", "state__label", "label"]
    readonly_fields = ["id", "created_at", "updated_at", "_is_deleted", "_deleted_at"]


@admin.register(Branch)
class BranchAdmin(BaseAdmin):
    list_display = ["code", "title", "city", "mobile", "is_active", "created_at"]
    list_filter = ["city", "city__state", "is_active"]
    search_fields = ["code", "title", "address", "mobile", "city__label"]
    ordering = ["city__state__country__label", "city__state__label", "city__label", "title"]
    readonly_fields = ["id", "created_at", "updated_at", "_is_deleted", "_deleted_at"]
    fieldsets = (
        (_("Basic Info"), {
            "fields": ("code", "title", "address", "location", "mobile")
        }),
        (_("Location"), {
            "fields": ("city",)
        }),
        (_("Status"), {
            "fields": ("is_active",)
        }),
        (_("System Fields"), {
            "fields": ("id", "created_at", "updated_at", "_is_deleted", "_deleted_at"),
            "classes": ("collapse",)
        }),
    )
