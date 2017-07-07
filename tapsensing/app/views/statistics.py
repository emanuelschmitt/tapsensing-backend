import datetime

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

    counts = [touches.count() for touches in filtered_by_date]
    labels = [date.strftime('%a') for date in d_range]

    return {
        'counts': counts[::-1],
        'labels': labels[::-1]
    }


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def statistics(request):
    last_n_days = 3

    counts_sensordata = last_n_days_count(SensorData, last_n_days, 'timestamp')
    counts_touch = last_n_days_count(TouchEvent, last_n_days,  'timestamp')
    counts_session = last_n_days_count(Session, last_n_days, 'date')

    response = {
        'sensor': counts_sensordata,
        'touch': counts_touch,
        'session': counts_session
    }

    return Response(response)
