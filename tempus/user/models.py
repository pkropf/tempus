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


from django.db import models
from django.contrib import admin
from datetime import datetime, date, timedelta
from django.core.exceptions import ValidationError


class Profile(models.Model):
    """collections of objects that identify a user
    note that the image should be of 1:1.33 ratio for best viewing
    """
    first_name           = models.CharField(max_length=64, help_text="Person's first name.")
    last_name            = models.CharField(max_length=64, help_text="Person's last name.")
    image                = models.ImageField(upload_to='profile/%Y/%m/%d', null=True, blank=True)
    email                = models.EmailField(help_text="User's email address.", null=True, blank=True)
    nick_name            = models.CharField(max_length=32, help_text="Person's nick name.", null=True, blank=True)
    cell_phone           = models.CharField(max_length=15, null=True, blank=True)
    home_phone           = models.CharField(max_length=15, null=True, blank=True)
    work_phone           = models.CharField(max_length=15, null=True, blank=True)
    emergency_first_name = models.CharField(max_length=64, help_text="Name of the emergency contact for the person.", null=True, blank=True)
    emergency_last_name  = models.CharField(max_length=64, help_text="Name of the emergency contact for the person.", null=True, blank=True)
    emergency_phone      = models.CharField(max_length=15, help_text="Phone number of the emergency contact for the person.", null=True, blank=True)


    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def timecard_urls(self):
        return [(t.timecardtype.name, '/api/v1/timecard/%d/' % t.pk) for t in self.timecard_set.order_by('timecardtype__name')]


class CrossName(models.Model):
    """Names of cross references.
    """
    name      = models.CharField(max_length=64, help_text="cross reference name")

    class Meta:
        verbose_name = 'Cross Reference Name'

    def __unicode__(self):
        return '%s' % (self.name)


class CrossReference(models.Model):
    """Cross reference to other systems.
    """
    name      = models.ForeignKey(CrossName)
    reference = models.IntegerField(db_index=True, help_text="cross reference id")
    profile   = models.ForeignKey(Profile)

    class Meta:
        unique_together = (("name", "profile"),)
        verbose_name = 'Cross Reference'

    def __unicode__(self):
        return '%s - %d - %s' % (self.name, self.reference, self.profile)
