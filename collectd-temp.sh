#!/bin/sh
HOSTNAME="${COLLECTD_HOSTNAME:-localhost}"
INTERVAL="${COLLECTD_INTERVAL:-10}"
ID=$1

VALUE=$(cat /sys/bus/w1/devices/28-$ID/w1_slave |grep t= |awk -F'=' '{print $NF/1000}')
echo "PUTVAL \"$HOSTNAME/exec-temp/temperature-$ID\" interval=$INTERVAL N:$VALUE"

