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
from tempus.user.models import Profile
from django.contrib.auth.models import User
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpApplicationError
from django.core.exceptions import ValidationError


class ProfileResource(ModelResource):
    #rfid = fields.ForeignKey(RfidcardResource, 'rfid')
    #timecard = fields.ToManyField('timecard.api.TimecardResource', 'timecard')
    timecards = fields.ListField(readonly = True)

    class Meta:
        queryset = Profile.objects.all()
        resource_name = 'profile'
        #authentication = BasicAuthentication()
        authentication = Authentication()
        filtering = {
            'first_name': ALL,
            'last_name': ALL,
            'email': ALL,
            }
        ordering = ['tag',]

    def dehydrate_timecards(self, bundle):
        return bundle.obj.timecard_urls()
