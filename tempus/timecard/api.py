# -*- coding: utf-8 -*-

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


from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from timecard.models import Rfidcard, Profile, TimecardType, Timecard, Stamp
from django.contrib.auth.models import User


class RfidcardResource(ModelResource):
    class Meta:
        queryset = Rfidcard.objects.all()
        resource_name = 'rfidcard'
        authentication = BasicAuthentication()
        ordering = ['rfid',]
        filtering = {
            'rfid': ALL,
            }


class ProfileResource(ModelResource):
    rfid = fields.ForeignKey(RfidcardResource, 'rfid')
    #timecard = fields.ToManyField('timecard.api.TimecardResource', 'timecard')
    timecards = fields.ListField(readonly = True)

    class Meta:
        queryset = Profile.objects.all()
        resource_name = 'profile'
        authentication = BasicAuthentication()
        filtering = {
            'rfid': ALL_WITH_RELATIONS,
            'first_name': ALL,
            'last_name': ALL,
            'email': ALL,
            }
        ordering = ['tag',]

    def dehydrate_timecards(self, bundle):
        return bundle.obj.timecard_urls()




class TimecardTypeResource(ModelResource):
    class Meta:
        queryset = TimecardType.objects.all()
        resource_name = 'timecardtype'
        authentication = BasicAuthentication()
        ordering = ['name',]


class TimecardResource(ModelResource):
    class Meta:
        queryset = Timecard.objects.all()
        resource_name = 'timecard'
        authentication = BasicAuthentication()
        filtering = {
            'profile': ALL_WITH_RELATIONS,
            }

    hours_today  = fields.FloatField(readonly = True)
    hours_total  = fields.FloatField(readonly = True)
    pairs        = fields.ListField(readonly = True)
    typename     = fields.CharField(readonly = True)
    timecardtype = fields.ForeignKey(TimecardTypeResource, 'timecardtype')
    profile      = fields.ForeignKey(ProfileResource, 'profile')


    def dehydrate_hours_today(self, bundle):
        return bundle.obj.hours_today()


    def dehydrate_hours_total(self, bundle):
        return bundle.obj.hours()


    def dehydrate_pairs(self, bundle):
        return bundle.obj.pairs()


    def dehydrate_typename(self, bundle):
        return bundle.obj.timecardtype.name



class StampResource(ModelResource):
    class Meta:
        queryset = Stamp.objects.all()
        resource_name = 'stamp'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        ordering = ['stamp',]

    timecard = fields.ToOneField(TimecardResource, 'timecard')
