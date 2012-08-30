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


from django.test import TestCase

import datetime
import warnings
from django.contrib.auth.models import User
from tastypie.test import ResourceTestCase
from django.utils import unittest
from timecard.models import Rfidcard, Profile, TimecardType


class RfidcardResourceTest(ResourceTestCase):
    def setUp(self):
        super(RfidcardResourceTest, self).setUp()

        self.username = 'Wilma'
        self.password = 'password'
        self.email    = 'wilma@example.com'
        self.user     = User.objects.create_user(self.username, self.email, self.password)

        self.rfid_1 = Rfidcard.objects.get(pk=1)
        self.detail_url = '/api/v1/rfidcard/{0}/'.format(self.rfid_1.pk)


    def get_credentials(self):
        return self.create_basic(username=self.username, password=self.password)


    def test_get_rfidcard(self):
        resp = self.api_client.get('/api/v1/rfidcard/', format='json', authentication=self.get_credentials())

        self.assertValidJSONResponse(resp)

        self.assertEqual(len(self.deserialize(resp)['objects']), 2)


    def test_get_rfidcards_unauthorzied(self):
        self.assertHttpUnauthorized(self.api_client.get('/api/v1/rfidcard/', format='json'))
