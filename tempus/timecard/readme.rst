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


api interactions via command line
=================================

list profiles::

  $ curl --dump-header - -u peter:byteme -H 'Accept: application/json' http://localhost:8000/api/v1/profile/
  HTTP/1.0 200 OK
  Date: Thu, 13 Sep 2012 03:45:59 GMT
  Server: WSGIServer/0.1 Python/2.7.2
  Content-Type: application/json; charset=utf-8
  
  {"meta": {"limit": 20,
            "next": null,
            "offset": 0,
            "previous": null,
            "total_count": 2},
   "objects": [{"cell_phone": "4084829427",
                "email": "pkropf@gmail.com",
                "emergency_first_name": "",
                "emergency_last_name": "",
                "emergency_phone": "",
                "first_name": "Peter",
                "fm_id": null,
                "home_phone": "",
                "id": 1,
                "image": "/media/profile/2012/06/26/me2.png",
                "last_name": "Kropf",
                "nick_name": "",
                "resource_uri": "/api/v1/profile/1/",
                "rfid": "/api/v1/rfidcard/1/",
                "timecards": [["Create",
                               "/api/v1/timecard/2/"],
                              ["Faculty",
                               "/api/v1/timecard/4/"],
                              ["Staff",
                               "/api/v1/timecard/1/"]],
                "work_phone": ""},
               {"cell_phone": null,
                "email": null,
                "emergency_first_name": null,
                "emergency_last_name": null,
                "emergency_phone": null,
                "first_name": "Mocha",
                "fm_id": null,
                "home_phone": null,
                "id": 2,
                "image": "/media/profile/2012/09/12/Mocha.jpg",
                "last_name": "Kropf",
                "nick_name": null,
                "resource_uri": "/api/v1/profile/2/",
                "rfid": "/api/v1/rfidcard/2/",
                "timecards": [["Create",
                               "/api/v1/timecard/5/"]],
                "work_phone": null}]}
  $


lookup a profile::

  $ curl --dump-header - -u peter:byteme -H 'Accept: application/json' http://localhost:8000/api/v1/profile/1/
  HTTP/1.0 200 OK
  Date: Tue, 11 Sep 2012 20:06:39 GMT
  Server: WSGIServer/0.1 Python/2.7.2
  Content-Type: application/json; charset=utf-8
  
  {"id": 1,
   "image": null,
   "resource_uri": "/api/v1/profile/1/",
   "rfid": "/api/v1/rfidcard/1/",
   "tag": "peter",
   "user": "/api/v1/user/1/"}
  $


lookup a profile by rfid::

  $ curl --dump-header - -u peter:byteme -H 'Accept: application/json' http://localhost:8000/api/v1/profile/?rfid__rfid=4C0020F73B
  HTTP/1.0 200 OK
  Date: Thu, 13 Sep 2012 02:35:28 GMT
  Server: WSGIServer/0.1 Python/2.7.2
  Content-Type: application/json; charset=utf-8
  
  {"meta": {"limit": 20,
            "next": null,
            "offset": 0,
            "previous": null,
            "total_count": 1},
   "objects": [{"id": 1,
                "image": null,
                "resource_uri": "/api/v1/profile/1/",
                "rfid": "/api/v1/rfidcard/1/",
                "tag": "peter",
                "timecards": [["Create",
                               "/api/v1/timecard/2/"],
                              ["Faculty",
                               "/api/v1/timecard/4/"],
                              ["Staff",
                               "/api/v1/timecard/1/"]],
                "user": "/api/v1/user/1/"}]}
  $ 


search for profiles by first name::

  $ curl --dump-header - -u peter:byteme -H 'Accept: application/json' http://localhost:8000/api/v1/profile/?first_name=peter
  HTTP/1.0 200 OK
  Date: Thu, 13 Sep 2012 03:51:14 GMT
  Server: WSGIServer/0.1 Python/2.7.2
  Content-Type: application/json; charset=utf-8
  
  {"meta": {"limit": 20,
           "next": null,
           "offset": 0,
           "previous": null,
           "total_count": 0},
           "objects": []}
  $
  $ curl --dump-header - -u peter:byteme -H 'Accept: application/json' http://localhost:8000/api/v1/profile/?first_name=Peter
  HTTP/1.0 200 OK
  Date: Thu, 13 Sep 2012 03:51:21 GMT
  Server: WSGIServer/0.1 Python/2.7.2
  Content-Type: application/json; charset=utf-8
  
  {"meta": {"limit": 20,
            "next": null,
            "offset": 0,
            "previous": null,
            "total_count": 1},
   "objects": [{"cell_phone": "4084829427",
                "email": "pkropf@gmail.com",
                "emergency_first_name": "",
                "emergency_last_name": "",
                "emergency_phone": "",
                "first_name": "Peter",
                "fm_id": null,
                "home_phone": "",
                "id": 1,
                "image": "/media/profile/2012/06/26/me2.png",
                "last_name": "Kropf",
                "nick_name": "",
                "resource_uri": "/api/v1/profile/1/",
                "rfid": "/api/v1/rfidcard/1/",
                "timecards": [["Create",
                               "/api/v1/timecard/2/"],
                              ["Faculty",
                               "/api/v1/timecard/4/"],
                              ["Staff",
                               "/api/v1/timecard/1/"]],
                "work_phone": ""}]}
  $
  
  
lookup the timecard(s) for a profile::

  $ curl --dump-header - -u peter:byteme -H 'Accept: application/json' http://localhost:8000/api/v1/timecard/?profile=1
  HTTP/1.0 200 OK
  Date: Tue, 11 Sep 2012 20:16:20 GMT
  Server: WSGIServer/0.1 Python/2.7.2
  Content-Type: application/json; charset=utf-8
  
  {"meta": {"limit": 20,
            "next": null,
            "offset": 0,
            "previous": null,
            "total_count": 3},
   "objects": [{"end_date": "2012-12-31",
                "hours_today": 0,
                "hours_total": 0,
                "id": 4,
                "notes": "",
                "pairs": [["60: 2012-09-11 12:52:43.801171",
                           null]],
                "profile": "/api/v1/profile/1/",
                "resource_uri": "/api/v1/timecard/4/",
                "start_date": "2012-01-01",
                "timecardtype": "/api/v1/timecardtype/5/",
                "typename": "Faculty"},
               {"end_date": "2013-08-30",
                "hours_today": 0.041666666666666664,
                "hours_total": 22.172500000000003,
                "id": 1,
                "notes": "",
                "pairs": [["1: 2012-08-29 14:07:40",
                           "2: 2012-08-29 22:08:07"],
                          ["3: 2012-08-30 08:22:05",
                           "4: 2012-08-30 22:22:22"],
                          ["5: 2012-08-30 22:27:37",
                           null],
                          ["61: 2012-09-11 13:05:35.261861",
                           null]],
                "profile": "/api/v1/profile/1/",
                "resource_uri": "/api/v1/timecard/1/",
                "start_date": "2012-08-29",
                "timecardtype": "/api/v1/timecardtype/4/",
                "typename": "Staff"},
               {"end_date": "2013-08-31",
                "hours_today": 0.0005555555555555556,
                "hours_total": 0.0005555555555555556,
                "id": 2,
                "notes": "",
                "pairs": [["7: 2012-08-31 23:37:32.933185",
                           null],
                          ["58: 2012-09-11 12:48:51.878007",
                           "59: 2012-09-11 12:48:54.664882"]],
                "profile": "/api/v1/profile/1/",
                "resource_uri": "/api/v1/timecard/2/",
                "start_date": "2012-08-31",
                "timecardtype": "/api/v1/timecardtype/2/",
                "typename": "Create"}]}
  $


stamp a timecard::

  $ curl --dump-header - -u peter:byteme -H "Content-Type: application/json" -X POST --data '{"timecard": "/api/v1/timecard/1/"}' http://localhost:8000/api/v1/stamp/
  HTTP/1.0 201 CREATED
  Date: Tue, 11 Sep 2012 20:05:35 GMT
  Server: WSGIServer/0.1 Python/2.7.2
  Content-Type: text/html; charset=utf-8
  Location: http://localhost:8000/api/v1/stamp/61/
  
  $
