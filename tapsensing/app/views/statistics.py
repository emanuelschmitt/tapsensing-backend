import datetime

from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import TouchEvent, SensorData, Session


def date_range(last_n):
    """returns array with datetimes for the last_n days"""
    today = datetime.date.today()
    timedeltas = [datetime.timedelta(days=x) for x in range(last_n)]
    dates = [today - delta for delta in timedeltas]
    return dates


def _24_hour_range():
    today = datetime.datetime.now()
    timedeltas = [datetime.timedelta(hours=x) for x in range(24)]
    dates = [today - delta for delta in timedeltas]
    return dates


def filter_by_hour(queryset, date):
    field_dict = {
        'timestamp__day': date.day,
        'timestamp__month': date.month,
        'timestamp__year': date.year,
        'timestamp__hour': date.hour
    }

    return queryset.filter(**field_dict)


def filter_by_day(queryset, date, datefield):
    """filters an ORM queryset to match exact date"""

    field_dict = {
        '{}__day'.format(datefield): date.day,
        '{}__month'.format(datefield): date.month,
        '{}__year'.format(datefield): date.year
    }

    return queryset.filter(**field_dict)


def last_n_days_count(model, n_days, datefield):
    """
    Counts the amount of objects for a certain model for each last_n days
    returns dict with dates as y and the counts as x for plotting
    """
    queryset = model.objects.all()
    d_range = date_range(n_days)
    filtered_by_date = [filter_by_day(queryset, date, datefield) for date in d_range]

    counts = [objects.count() for objects in filtered_by_date]
    labels = [date.strftime('%a') for date in d_range]

    return {
        'counts': counts[::-1],
        'labels': labels[::-1]
    }


def last_24_hours_count(model):
    queryset = model.objects.all()
    d_range = _24_hour_range()
    filtered_by_date = [filter_by_hour(queryset, date) for date in d_range]

    counts = [objects.count() for objects in filtered_by_date]
    labels = [date.strftime('%Hh') for date in d_range]

    return {
        'counts': counts[::-1],
        'labels': labels[::-1]
    }


def users_participated():
    # TODO: filter users here
    user_count = User.objects.count()
    today = datetime.date.today()

    sessions_today = filter_by_day(
        Session.objects,
        today,
        'date'
    )

    unique_users_participated = [session.user.id for session in sessions_today]
    unique_users_participated = len(list(set(unique_users_participated)))

    return {
        'counts': [unique_users_participated, user_count],
        'labels': ['participated', 'total']
    }


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def statistics(request):
    last_n_days = 7

    counts_sensordata_week = last_n_days_count(SensorData, last_n_days, 'timestamp')
    counts_touch_week = last_n_days_count(TouchEvent, last_n_days, 'timestamp')
    counts_session_week = last_n_days_count(Session, last_n_days, 'date')

    counts_sensor_data_24 = last_24_hours_count(SensorData)
    counts_touch_24 = last_24_hours_count(TouchEvent)

    response = {
        'sensorWeek': counts_sensordata_week,
        'touchWeek': counts_touch_week,
        'sessionWeek': counts_session_week,
        'touch24': counts_touch_24,
        'sensor24': counts_sensor_data_24,
        'usersParticipated': users_participated()
    }

    return Response(response)
