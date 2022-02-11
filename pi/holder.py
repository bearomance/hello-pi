import os
import time
import yaml


def main():
    while True:

        time.sleep(60)

        # 判断网络是否通畅
        config = yaml.safe_load(open('/home/pi/piAgent/pi/config.yml'))
        ip = config['kafka']['server']
        result = os.system("ping {} -c 3".format(ip))
        if result != 0:
            os.system("sudo reboot")

        # 判断monitor进程是否正常
        process = len(os.popen('ps aux | grep "' + 'monitor' + '" | grep -v grep').readlines())
        if process < 1:
            os.system('sudo reboot')


if __name__ == '__main__':
    main()
