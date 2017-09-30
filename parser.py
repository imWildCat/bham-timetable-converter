from pyquery import PyQuery as pq

from datetime import datetime
import datetime as dt
import pytz

from icalendar import Calendar, Event, vText


def parse(html_string):
    doc = pq(html_string)

    day = 0
    lectures = []

    for i in range(2, 7):
        day += 1
        es = doc('table.grid-border-args tr:nth-child({}) > td.cell-border, table.grid-border-args tr:nth-child({}) > td.Lecture'.format(i, i))
        print(es)
        lectures += parse_day(es, day)

    return make_ical(lectures)


def parse_day(cells, day):
    lectures = []

    time = 9
#     print('day:', day)
    for e in cells:

        pq_e = pq(e)
        class_name = pq_e.attr('class')

        if class_name == 'Lecture':
            class_start_time = int(time)

            title = pq(e)('table:nth-child(1) td:nth-child(1)').text()
            tutor = pq(e)('table:nth-child(2) td:nth-child(1)').text()
            location = pq(e)('table:nth-child(2) td:nth-child(2)').text()
            duration = pq(e)('table:nth-child(3) td:nth-child(1)').text()

            # print(title)
            # print(tutor)
            # print(location)
            # print(duration)

#             print(pq_e)

            _d = int(pq_e.attr('colspan')) * 0.5

            time += _d

            class_end_time = int(time)


#             print('starts at: {}, ends at: {}'.format(class_start_time, class_end_time))

#             print('===')

            print('duration:', duration)
            lectures.append((title, tutor, location, duration,
                             day, class_start_time, class_end_time))
        else:
            #             print('add 0.5')
            time += 0.5

    return lectures


def make_ical(lectures):
    cal = Calendar()

    cal.add('prodid', '-//My calendar product//mxm.dk//')
    cal.add('version', '2.0')

    cal['summary'] = 'foo'

    start_date = 2

    for week in range(2, 12):
        for (title, tutor, location, duration, day, start, end) in lectures:

            start_time = datetime(2017, 10, start_date - 1 + day,
                                  start, 0, tzinfo=pytz.timezone('Europe/London'))
            end_time = datetime(2017, 10, start_date - 1 + day,
                                end, 0, tzinfo=pytz.timezone('Europe/London'))
            if week > 2:
                delta = dt.timedelta(days=7 * (week - 2))
                start_time += delta
                end_time += delta

            event = Event()
            event.add('summary', '{} ({})'.format(title, duration))
            event.add('dtstart', start_time)
            event.add('dtend', end_time)
            event['location'] = vText('{} (may change)'.format(location))

            cal.add_component(event)

    return cal.to_ical()
