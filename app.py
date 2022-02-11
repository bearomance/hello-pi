from flask import Flask, request
import py_eureka_client.eureka_client as eureka_client
import paramiko


def execute_remote(hostname, username, password, cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname, port=22, username=username, password=password)
    for c in cmd:
        client.exec_command(c)
    client.close()


app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello Raspberry Pi!'


@app.route('/reboot')
def reboot():
    ip = request.data
    execute_remote(ip, 'pi', 'raspberry', ['sudo reboot'])


if __name__ == '__main__':
    eureka_client.init(eureka_server='http://name:password@127.0.0.1:8761/eureka/',
                       app_name='piagent',
                       instance_host='127.0.0.1',
                       instance_port='9091',
                       ha_strategy=eureka_client.HA_STRATEGY_RANDOM)

    app.run(host='0.0.0.0', port=8888)
