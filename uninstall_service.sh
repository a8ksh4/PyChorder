#!/bin/sh

systemctl disable keyboard.service
rm /etc/systemd/system/keyboard.service
