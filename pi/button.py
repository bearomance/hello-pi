# 按钮控制蜂鸣器

from gpiozero import Button, Buzzer
from signal import pause
import yaml


def main():
    config = yaml.safe_load(open('/home/pi/piAgent/pi/config.yml'))

    if config['sensor']['button']['start']:
        buzzer = Buzzer(config['sensor']['buzzer']['gpio'])
        button = Button(config['sensor']['button']['gpio'])
        button.when_activated = buzzer.off

        pause()


if __name__ == '__main__':
    main()
