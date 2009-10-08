# coding=utf-8
from django.contrib import admin
from models import *

class StateAdmin(admin.ModelAdmin):
    model = State
    list_display = ('name','abbr')
    ordering = ('name',)

    fieldsets = (
        (None, {'fields': ('name', ('abbr', 'slug'), 'ap_style')}),
        ('Location', {'fields': ('poly',)}),
    )
    prepopulated_fields = {"slug": ("abbr",)}
    search_fields = ('name','abbr','ap_style')
admin.site.register(State,StateAdmin)

class CountyAdmin(admin.ModelAdmin):
    model = County
    list_display = ('name','state','long_name')
    list_filter  = ('state',)
    ordering = ('name',)

    fieldsets = (
        (None, {'fields': (('name','slug'),'state','long_name')}),
        ('Metadata', {'fields': ('fips_code',)}),
        ('Location', {'fields': ('poly',)}),
    )
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name','state__name','long_name')
admin.site.register(County,CountyAdmin)

class ZipCodeAdmin(admin.ModelAdmin):
    model = ZipCode
    list_display = ('name','state')
    ordering = ('name',)

    fieldsets = (
        (None, {'fields': (('name', 'slug'))}),
        ('Location', {'fields': ('poly',)}),
    )
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name','state__name')
admin.site.register(ZipCode,ZipCodeAdmin)

