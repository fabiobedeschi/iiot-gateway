from os import getenv

from .src.subscriber import Subscriber

if __name__ == '__main__':
    subscriber = Subscriber()
    subscriber.connect(
        host=getenv('USERSERVICE_HOST'),
        port=int(getenv('USERSERVICE_PORT', 1883)),
        keepalive=int(getenv('USERSERVICE_KA', 60))
    )
    subscriber.loop_forever()
