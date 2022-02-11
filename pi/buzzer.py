import socket
import logging
import yaml
from gpiozero import Buzzer
from kafka import KafkaConsumer

logging.basicConfig(filename='/home/pi/piAgent/s2.log', level=logging.ERROR)


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address


def main():
    config = yaml.safe_load(open('/home/pi/piAgent/config.yml'))

    ip = get_ip_address()

    # 消费告警队列
    consumer = KafkaConsumer(config['kafka']['alarm_topic'],
                             bootstrap_servers=config['kafka']['server'],
                             auto_offset_reset='latest')

    # print('wait for alarm...')
    buzzer = Buzzer(config['sensor']['buzzer']['gpio'])
    for msg in consumer:
        # print(msg)
        try:
            value = msg.value.decode('utf-8')
            data = value.split('_')
            if ip == data[0]:
                alarm = data[1]
                if alarm == '0':
                    buzzer.on()
                else:
                    buzzer.off()
        except Exception as e:
            logging.error(str(e))


if __name__ == "__main__":
    main()
