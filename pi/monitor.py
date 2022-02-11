# 监控：温湿度、气体
import json
import logging
import socket
import time
import uuid
import smbus
import yaml
from kafka import KafkaProducer

logging.basicConfig(filename='/home/pi/piAgent/pi/monitor.log', level=logging.ERROR)

config = yaml.safe_load(open('/home/pi/piAgent/pi/config.yml'))
producer = KafkaProducer(bootstrap_servers=[config['kafka']['server']],
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))


def get_mac_address():
    _mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([_mac[e:e + 2] for e in range(0, 11, 2)])


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address


def get_tenant_id_by_config():
    return config['tenant_id']


def get_tenant_id_by_file():
    try:
        file = open("/home/pi/tenant.txt")
        lines = file.readlines()
        return ''.join(lines).strip('\n')
    except FileNotFoundError:
        print("File not found")
    except PermissionError:
        print("Permission error")
    finally:
        return '1'


ip = get_ip_address()
tenant_id = get_tenant_id_by_config()
mac = get_mac_address()


def send_mq(tag, value):
    d = {
        'time': time.time(),
        'tag': config['kafka']['prefix'] + tag,
        'value': value,
        'ip': ip,
        'tenantId': tenant_id,
        'mac': mac
    }
    future = producer.send(config['kafka']['monitor_topic'], d)
    future.get(timeout=10)


def send_error(e, ip):
    d = {
        'time': time.time(),
        'error': e,
        'ip': ip
    }
    future = producer.send(config['kafka']['error_topic'], d)
    future.get(timeout=10)


def main():
    monitor_temp = config['sensor']['temp_humi']
    monitor_air = config['sensor']['air']

    i2c = smbus.SMBus(1)

    temp_addr = 0x44
    air_addr = 0x58

    if monitor_temp:
        i2c.write_byte_data(temp_addr, 0x23, 0x34)
    if monitor_air:
        i2c.write_i2c_block_data(air_addr, 0x20, [0x03])
    time.sleep(0.5)

    reply_buffer = [0, 0, 0, 0, 0, 0]
    reply = [0, 0]

    error_count = 0

    while 1:
        try:
            # 监控温湿度
            if monitor_temp:
                i2c.write_byte_data(temp_addr, 0xe0, 0x0)
                time.sleep(0.6)

                data = i2c.read_i2c_block_data(temp_addr, 0x0, 6)
                rawT = ((data[0]) << 8) | (data[1])
                rawR = ((data[3]) << 8) | (data[4])

                temperature = -45 + rawT * 175 / 65535
                send_mq('temperature', temperature)

                RH = 100 * rawR / 65535
                send_mq('humidity', RH)

            # 监控气体
            if monitor_air:

                i2c.write_i2c_block_data(air_addr, 0x20, [0x08])
                time.sleep(0.6)

                air_data = i2c.read_i2c_block_data(air_addr, 0)
                for i in range(0, 6):
                    reply_buffer[i] = air_data[i]
                for i in range(0, 2):
                    reply[i] = reply_buffer[i * 3]
                    reply[i] <<= 8
                    reply[i] |= reply_buffer[i * 3 + 1]

                co2 = reply[0]
                tvoc = reply[1]

                send_mq('co2', co2)
                send_mq('tvoc', tvoc)

        except BaseException as e:
            send_error(str(e), ip)
            error_count = error_count + 1
        finally:
            time.sleep(15)


if __name__ == '__main__':
    main()
