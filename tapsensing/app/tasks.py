from push_notifications.models import APNSDevice

from background_task import background
from logging import getLogger

logger = getLogger(__name__)


@background(schedule=60)
def demo_task(message):
    print("jojojo")
    logger.debug('demo_task. message={0}'.format(message))


@background(schedule=60)
def send_push_notifications():
    logger.info('Sending push notifications...')

    devices = APNSDevice.objects.all()

    message = {
        'sound': 'default',
        'message': 'this is a test'
    }

    for device in devices:
        logger.info('Sending push notification to %d.' % device.user.id)
        device.send_message(
            message['message'],
            sound=message['sound']
        )
