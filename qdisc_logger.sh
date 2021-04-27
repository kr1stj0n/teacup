#!/bin/sh
# Copyright (c) 2013-2015 Centre for Advanced Internet Architectures,
# Swinburne University of Technology. All rights reserved.
#
# Author: Kr1stj0n C1k0 (kristjoc@ifi.uio.no)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
# log qdisc stats
#
# $Id: qdisc_logger.sh,v e7ea179b29d8 2021/04/27 04:28:23 kristjoc $

if [ $# -lt 3 -o $# -gt 4 ] ; then
        echo "Usage: $0 <interval> <iface> <qdisc ><log_file>"
        echo "          <interval>      poll interval as fraction of seconds"
        echo "          <iface>         router interface to collect stats from"
        echo "          <qdisc>         qdisc scheduler type"
        echo "          <log_file>      log file to write the data to"
        exit 1
fi

# Poll interval in seconds
INTERVAL=$1
# Interface
INTERFACE=$2
# Qdisc scheduler
QDISC=$3
# Log file
LOG_FILE=$4

rm -f $LOG_FILE

while [ 1 ] ; do
	TIME_1=`date +%s.%N`
	CMD="tc -s qdisc show dev ${INTERFACE} | sed -n '/${QDISC}/,$p'"
        OUTPUT=$(eval $CMD)
	echo "$TIME_1" >> $LOG_FILE
	echo " " >> $LOG_FILE

        QLEN=$(echo "$OUTPUT" | grep -Po 'backlog \K.*' | awk '{print ($2+0)}')
        QDELAY=$(echo "$OUTPUT" | grep -Po 'qdelay \K.*' | awk '{print ($1+0)}')

        echo "$QLEN" >> $LOG_FILE
	echo " " >> $LOG_FILE

        echo "$QDELAY" >> $LOG_FILE
	TIME_2=`date +%s.%N`
	SLEEP_TIME=`echo $TIME_1 $TIME_2 $INTERVAL | awk '{ st = $3 - ($2 - $1) ; if ( st < 0 ) st = 0 ; print st }'`
	sleep $SLEEP_TIME
done
