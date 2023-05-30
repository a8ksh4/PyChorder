#!/bin/sh -x

cp ./battery.service /etc/systemd/system
systemctl enable battery.service