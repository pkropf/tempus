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
from tempus.user.models import Profile
from simple_history.models import HistoricalRecords



class Rfidcard(models.Model):
    """0100E2850E68"""

    rfid = models.CharField(max_length=24)
    active = models.BooleanField()
    profile = models.ForeignKey(Profile, null = True, blank = True)

    history = HistoricalRecords()

    def __unicode__(self):
        return self.rfid



class TimecardType(models.Model):
    """
    """

    name = models.CharField(max_length=64)
    ranking = models.IntegerField(unique=True)
    description = models.TextField(help_text = 'Description of the type of timecard.', null = True, blank = True)

    history = HistoricalRecords()


    def __unicode__(self):
        return self.name



class Timecard(models.Model):
    """A timecard is used to collet the stamps for a particular period
    of time. For instance, the all the times that a volunteer has
    clocked in and out.
    """

    timecardtype  = models.ForeignKey(TimecardType)
    profile       = models.ForeignKey(Profile)
    start_date    = models.DateField(help_text="The starting date for the timecard.")
    end_date      = models.DateField(help_text="The ending date for the timecard.")
    notes         = models.TextField(help_text="Notes on the timecard.", null=True, blank=True)

    history = HistoricalRecords()

    start_date.current_filter = True


    class Meta:
        ordering = ['profile', 'start_date']


    def __unicode__(self):
        return str(self.profile) + ': ' + str(self.timecardtype) + ' - ' + str(self.start_date) + ' - ' + str(self.end_date)


    def stampcard(self):
        """Add a stamp to the card.
        """

        Stamp(timecard = self).save()


    def hours_today(self):
        """Determine the number of hours logged today.
        """

        return self.hours(date.today())


    def pairs(self, day=None):
        """create a list of paired stamps. the pair is (older_stamp,
        younger_stamp). if a particular stamp doesn't have a partner,
        set it to none. stamps are considered paired if:

            * they both occur on the same day
            * [within 24 hours?]

        if there are more than 2 stamps on the same day, multiple
        pairs will be created.
        """

        p = []
        c = None
        if day:
            stamps = self.stamp_set.filter(stamp__year = day.year, stamp__month = day.month, stamp__day = day.day).order_by('stamp')

        else:
            stamps = self.stamp_set.order_by('stamp')


        for s in stamps:
            if c == None:
                c = s
                continue

            if s.stamp.date() == c.stamp.date():
                p.insert(0, (c, s))
                c = None

            else:
                p.insert(0, (c, None))
                c = s

        if c != None:
            p.insert(0, (c, None))

        return p


    def hours(self, day=None):
        """Determine the number of hours logged on the timecard. if
        day is specified, the hours are return for that day. otherwise
        it's for the timecard.
        """

        h = sum([(c.stamp - o.stamp).seconds / 60. / 60. for o, c in self.pairs(day) if c != None])

        return float("%0.2f" % h)



class Stamp(models.Model):
    """A stamp provides the basis for recording the time someone
    clocks in and then clocks out.
    """

    stamp = models.DateTimeField(help_text="Clock date and time.")
    timecard = models.ForeignKey('Timecard')

    history = HistoricalRecords()


    def __unicode__(self):
        return str(self.id) + ': ' + str(self.stamp)


    def clean(self, *args, **kwargs):
        if not self.id:
            if self.timecard.start_date > self.stamp.date():
                raise ValidationError('Timecard in inactive: %s' % self.timecard)

            if self.stamp.date() > self.timecard.end_date:
                raise ValidationError('Timecard has expired: %s' % self.timecard)

        super(Stamp, self).clean(*args, **kwargs)


    def full_clean(self, *args, **kwargs):
        return self.clean(*args, **kwargs)


    def save(self):
        if not self.id:
            self.stamp = datetime.now()

        self.full_clean()
        super(Stamp, self).save()
