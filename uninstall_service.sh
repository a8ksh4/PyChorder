#!/bin/sh

systemctl disable battery.service
rm /etc/systemd/system/battery.service