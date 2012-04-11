Background
==========

Timecards have a start and end date. 

Timecards have a type.

Timecards collect timestamps.

Users have timecards. 

Users can have more than one active timecard.

Users cannot have more than one active timecard of the same type.

Users can have more than one expired timecard.

Users have one active rfid card.

Users can have more than one inactive rfid card.


Scenario 1
----------

A user with one active timecard.

When the card is swiped at the timecard station, a timestamp is added
to the card. A short message is displayed showing the user's name and
the timestamp.


Scenario 2
----------

A user with no active timecards and one expired timecard.

When the card is swiped at the timecard station, an error is displayed
that there is no active timecard.


Scenario 3
----------

A user with multiple active timecards.

When the card is swiped at the timecard station, the user is given a
choice of which timecard to be stamped.
