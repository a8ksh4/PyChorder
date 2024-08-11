#!/bin/sh -x

cp ./keyboard.service /etc/systemd/system
systemctl enable keyboard.service
