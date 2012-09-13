# Copyright (c) 2012 Peter Kropf. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


from models import Profile, Rfidcard, TimecardType, Timecard, Stamp
from django.contrib import admin


class ProfileAdmin(admin.ModelAdmin):
    list_display  = ('first_name', 'last_name', 'email', 'rfid',)
    ordering      = ('first_name', 'last_name', 'email', 'rfid',)
    search_fields = ('first_name', 'last_name', 'email', 'rfid',)

admin.site.register(Profile, ProfileAdmin)


class RfidcardAdmin(admin.ModelAdmin):
    list_display  = ('rfid', 'active',)
    ordering      = ('rfid',)
    search_fields = ('rfid',)

admin.site.register(Rfidcard, RfidcardAdmin)


class TimecardTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering     = ('name',)
    search_fields = ('name',)

admin.site.register(TimecardType, TimecardTypeAdmin)


class TimecardAdmin(admin.ModelAdmin):
    list_display  = ('profile', 'timecardtype', 'start_date', 'end_date',)
    ordering      = ('profile', 'start_date',)
    search_fields = ('profile__first_name', 'profile__last_name',)
    list_filter   = ('timecardtype', 'start_date', 'profile',)
    fieldsets     = (
        (None, {
            'fields': (
                ('timecardtype', 'profile',),
                ('start_date', 'end_date',),
                'notes',
                )
        }),)

admin.site.register(Timecard, TimecardAdmin)


class StampAdmin(admin.ModelAdmin):
    list_display = ('stamp', 'timecard',)
    ordering     = ('timecard',)
    search_fields = ('stamp', 'timecard',)

admin.site.register(Stamp, StampAdmin)
