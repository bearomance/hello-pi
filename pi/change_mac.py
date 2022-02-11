import os
import random
import time


def random_mac():
    mac = [0x00, 0xe0, 0x4c,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))


def main():
    rc_file = "/etc/rc.local"
    fd = open(rc_file).readlines()
    i = 1
    edit_flag = False

    for line in fd:
        print('{}: {}'.format(i, line))
        i = i + 1
        if line.startswith('ifconfig'):
            edit_flag = True
            break

    if not edit_flag:
        end = fd.pop()
        fd.append('ifconfig eth0 down\n')
        fd.append('ifconfig eth0 hw ether {}\n'.format(random_mac()))
        fd.append('ifconfig eth0 up\n\n')
        fd.append(end)

        fc = open(rc_file, 'w')
        fc.writelines(fd)
        fc.close()

        time.sleep(10)
        os.system("sudo reboot")


if __name__ == '__main__':
    main()
