#!/bin/sh
# Description: Starts Python scripts
### BEGIN INIT INFO
# Provides: Scripts
# Required-Start: $network $local_fs $syslog
# Required-Stop: $local_fs $syslog
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Description: Start Python scripts
### END INIT INFO

case $1 in
  start)
./teledaemon.py start
;;
  stop)
./teledaemon.py stop
;;
  restart)
./teledaemon.py restart
;;
  *)
 echo "Usage: scripts {start|stop|restart}"
exit 1
esac