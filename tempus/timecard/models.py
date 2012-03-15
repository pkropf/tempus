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
from django.contrib.auth.models import User, Group


class UserProfile(models.Model):
    # This is the only required field
    user  = models.ForeignKey(User, unique=True)
    image = models.ImageField(upload_to='profile/%Y/%m/%d', height_field='height', width_field='width', null=True, blank=True)


class Stamp(models.Model):
    """A stamp provides the basis for recording the time someone
    clocks in and then clocks out.
    """
    stamp_in  = models.DateTimeField(help_text="Clock date and time.")
    stamp_out = models.DateTimeField(help_text="Clock out date and time.", null=True, blank=True)
    card      = models.ForeignKey('Card')

    def __unicode__(self):
        return str(self.id) + ': ' + str(self.stamp_in) + ' - ' + str(self.stamp_out)

    def stamp(self):
        if self.stamp_in == None:
            self.stamp_in = datetime.now()
        elif self.stamp_out == None:
            self.stamp_out = datetime.now()

    def hours(self):
        """Determine the number of hours between the stamp in and out.
        """
        if self.stamp_in and self.stamp_out:
            t = self.stamp_out - self.stamp_in
            return t.days * 24 + (t.seconds / 60.0 / 60.0)
        else:
            return 0.0

    def admin_hours(self):
        return '%.2f' % self.hours()
    admin_hours.short_description = 'Stamp Hours'



class CardTypes(models.Model):
    """
    """
    name = models.CharField(max_length=64)
    description = models.TextField(help_text = 'Description of the type of time card.', null = True, blank = True)



class Card(models.Model):
    """A card is used to collet the stamps for a particular period of
    time. For instance, the all the times that a volunteer
    """
    card_type  = models.ForeignKey(CardTypes)
    user       = models.ForeignKey(User, null=True, blank=True)
    group      = models.ForeignKey(Group, null=True, blank=True)
    start_date = models.DateField(help_text="The starting date for the timecard.")
    end_date   = models.DateField(help_text="The ending date for the timecard.")
    notes      = models.TextField(help_text="Notes on the timecard.", null=True, blank=True)

    start_date.current_filter = True

    class Meta:
        ordering = ['user']

    def __unicode__(self):
        return str(self.person) + ': ' + str(self.start_date) + ' - ' + str(self.end_date)

    def stamp(self):
        open_stamps = Stamp.objects.filter(card=self, stamp_in__gte = date.today(), stamp_out = None)
        if len(open_stamps) == 0:
            stamp = Stamp(card = self)
        else:
            stamp = open_stamps[0]

        stamp.stamp()
        stamp.save()

    def hours(self):
        """Determine the number of hours logged on the card.
        """
        h = 0.0
        for s in Stamp.objects.filter(card=self):
            h = h + s.hours()

        return h

    def admin_hours(self):
        return '%.2f' % self.hours()
    admin_hours.short_description = 'Total Hours'

    def hours_today(self):
        """Determine the number of hours logged today.
        """
        h = 0.0
        for s in Stamp.objects.filter(card=self, stamp_in__gte = date.today()):
            h = h + s.hours()

        return h

    def hours_recorded(self):
        """Determine the number of hours recorded in the filemaker database for this timecard."""
        h = 0.0
        for rh in RecordedHours.objects.filter(card=self):
            h = h + rh.hours

        return h

    def hours_unrecorded(self):
        """Determine the number of hours not recorded in the filemaker database for this timecard."""
        return self.hours() - self.hours_recorded()
