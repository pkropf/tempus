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


from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tempus.timecard.models import Rfidcard, TimecardType, Timecard, Stamp
from tempus.user.api import ProfileResource
from django.contrib.auth.models import User
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpApplicationError
from django.core.exceptions import ValidationError


class RfidcardResource(ModelResource):
    class Meta:
        queryset = Rfidcard.objects.all()
        resource_name = 'rfidcard'
        #authentication = BasicAuthentication()
        authentication = Authentication()
        ordering = ['rfid',]
        filtering = {
            'rfid': ALL,
            }

    profile      = fields.ForeignKey(ProfileResource, 'profile')


class TimecardTypeResource(ModelResource):
    class Meta:
        queryset = TimecardType.objects.all()
        resource_name = 'timecardtype'
        #authentication = BasicAuthentication()
        authentication = Authentication()
        ordering = ['name',]


class TimecardResource(ModelResource):
    class Meta:
        queryset = Timecard.objects.all()
        resource_name = 'timecard'
        #authentication = BasicAuthentication()
        authentication = Authentication()
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
        # authentication = BasicAuthentication()
        authentication = Authentication()
        #authorization = DjangoAuthorization()
        authorization = Authorization()
        ordering = ['stamp',]

    timecard = fields.ToOneField(TimecardResource, 'timecard')

    def obj_create(self, bundle, **kwargs):
        try:
            b = super(StampResource, self).obj_create(bundle, **kwargs)

        except ValidationError as ve:
            raise ImmediateHttpResponse(HttpApplicationError(str(ve)))

        return b
