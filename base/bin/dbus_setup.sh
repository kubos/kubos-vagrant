#!/bin/bash

# Start D-Bus system daemon
if ! pgrep -x dbus-daemon > /dev/null
then
    dbus-daemon --config-file=/etc/dbus-1/kubos-dbus.conf --fork --nopidfile --address=unix:path=/tmp/kubos
fi

export DBUS_SESSION_BUS_ADDRESS="unix:path=/tmp/kubos"
export DBUS_STARTER_BUS_TYPE="session"
