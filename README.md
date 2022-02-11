# hello-pi
树莓派温湿度计

### 硬件
#### 传感器
##### 温湿度传感器SHT30
- Sensor VCC -> RaspberryPi 3.3v
- Sensor GND -> RaspberryPi Ground
- Sensor SDA -> RaspberryPi SDA (GPIO02)
- Sensor SCL -> RaspberryPi SCL (GPIO03)
##### 气体传感器SGP30
同温湿度传感器，将线并在一起后可以同时使用。
##### 蜂鸣器
- Sensor VCC -> RaspberryPi 3.3v
- Sensor I/O -> RaspberryPi GPIO
- Sensor GND -> RaspberryPi Ground
##### RGB LED灯
- Sensor RGB -> RaspberryPi GPIO
- Sensor GND -> RaspberryPi Ground
##### 开关
- Sensor S (SIG) -> RaspberryPi GPIO
- Sensor 中 (VCC) -> RaspberryPi 5v
- Sensor - (GND) -> RaspberryPi Ground

### 系统安装
#### 1. 下载系统
下载地址：<https://www.raspberrypi.org/downloads/raspbian/>

Desktop版本有桌面；Lite版本无桌面，根据需要下载。
#### 2. 烧录至TF卡
首先用[SD Card Formatter](https://www.sdcard.org/downloads/formatter/)将TF卡格式化。
然后使用balenaEtcher或Win32DiskImager等工具将刚刚下载的img系统烧录到TF卡中。
- [balenaEtcher](https://www.balena.io/etcher/)（Mac、Win）
- [Win32DiskImager](https://sourceforge.net/projects/win32diskimager/)（Win）

#### 3. 配置ssh
在boot文件夹中新建一个名为ssh的空白文件
``` shell
cd /Volumes/boot
touch ssh
```
#### 4. 配置WiFi
在boot文件夹下增加一个名为`wpa_supplicant.conf`的文件，加入以下内容：
``` shell
country=CN
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev 
update_config=1
network={
  ssid="MTS-Internet"
  key_mgmt=NONE
  priority=5
}
network={
ssid="xx"
psk="xxxxxxxxx"
key_mgmt=WPA-PSK
priority=4
}
```
### 系统配置
#### 安装开发环境
``` shell
sudo apt update
sudo apt install git vim python3-pip python3-gpiozero python3-smbus
pip3 install pyyaml
```
因为用pip3直接安装kafka-python有点问题，这里用源码的方式安装

```shell
git clone https://github.com/dpkp/kafka-python
pip3 install ./kafka-python
rm -rf kafka-python
```


#### 开启I2C
``` shell
sudo raspi-config
```
第5项：Interfacing Options
I2C，点击进入，点击Yes即可
#### 自启动
```shell
crontab -e
# 然后添加下面的命令
@reboot (/bin/sleep 30; /usr/bin/python3 /home/pi/script1.py  > /home/pi/cronjoblog 2>&1) 
```
### 常用命令
#### 树莓派命令
关机：sudo halt
重启：sudo reboot
在同一局域网下：`ping raspberrypi.local`可以找到树莓派的IP；
#### gpiozero


### 系统备份与恢复
备份：
``` shell
sudo dd if=/dev/rdisk2 | gzip>/Users/xmj/Documents/raspberry.gz
```

恢复：
``` shell
sudo gzip -dc raspberry.gz | sudo dd of=/dev/rdisk2
```

官网的：
sudo dd bs=4M if=/dev/sdb | gzip > raspbian.img.gz
gunzip --stdout raspbian.img.gz | sudo dd bs=4M of=/dev/sdb


```shell script
crontab -e

@reboot (/bin/sleep 30; /usr/bin/python3 /home/pi/piAgent/pi/monitor.py &)
@reboot (/bin/sleep 60; /usr/bin/python3 /home/pi/piAgent/pi/network_holder.py &)
```
