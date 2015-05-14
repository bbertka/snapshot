#!/bin/sh

if !(ps axho comm | grep snapshot.py > /dev/null)
then
(cd /root/scripts/snapshot && ./snapshot.py &)
fi
