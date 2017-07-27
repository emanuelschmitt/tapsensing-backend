from logging import getLogger
from datetime import date, time, datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from push_notifications.models import APNSDevice

from ...models import Session

logger = getLogger(__name__)

# set the time window where push notifications should be sent.
# NOTE: These are UTC Times, Berlin time is + 2h.
TIME_WINDOW_START = time(6, 0, 0)
TIME_WINDOW_END = time(21, 0, 0)

TIME_RANGES = [
    {
        # as the cronjob triggers, the cronjob is triggered once an our at XX:00
        # sending at 9:00 GMT+1
        'rng': [time(6, 30, 0), time(7, 30, 0)],
        'message': 'Good Morning. This a friendly reminder to take part in the tapsensing study today.',
        'sound': "default"
    },
    {
        # sending at 12:00 GMT+1
        'rng': [time(9, 30, 0), time(10, 30, 0)],
        'message': "Tapping is a lot of fun.",
        'sound': ""
    },
    {
        # sending at 18:00 GTM+1
        'rng': [time(15, 30, 0), time(16, 30, 0)],
        'message': "I know your day is busy, but don't forget to take part in the study.",
        'sound': ""
    },
    {
        # sending at 20:00 GTM+1
        'rng': [time(17, 30, 0), time(18, 30, 0)],
        'message': "",
        # default sound is the standard bling.
        'sound': "default"
    }
]


class Command(BaseCommand):
    help = 'Starts the push notifications.'

    def handle(self, *args, **options):
        send_push_notifications()


def send_push_notifications():
    now = datetime.now()
    now = now.time()
    logger.debug('It is now %s', now.strftime("%H:%M:%S"))

    # check if now is in the set time frame
    if not time_in_range(TIME_WINDOW_START, TIME_WINDOW_END, now):
        logger.info("Not sending push notifications because we are not in the time window")
        return

    logger.info('Sending push notifications...')

    # checking if we are in one of the timeranges
    for t_range in TIME_RANGES:
        if time_in_range(t_range['rng'][0], t_range['rng'][1], now):
            send_messages(t_range['message'], sound=t_range['sound'])
            break


def send_messages(message, sound='default'):
    users = User.objects.all()
    devices = APNSDevice.objects.all()

    for user in users:

        if does_session_exist_for_user(user.pk):
            continue

        user_devices = devices.filter(user=user)

        if not user_devices:
            continue

        logger.info('Sending push notification to %d.' % user.pk)
        user_devices.send_message(message, sound=sound)


def does_session_exist_for_user(user_id):
    today = date.today()
    return Session.objects.filter(date=today, user=user_id).exists()


def time_in_range(start, end, now):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= now <= end
    else:
        return start <= now or now <= end
