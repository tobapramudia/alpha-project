#!/bin/sh

if [ ! -f "/etc/ssh/ssh_host_rsa_key" ]; then
	# generate fresh rsa key
	ssh-keygen -f /etc/ssh/ssh_host_rsa_key -N '' -t rsa  -q -P ""
	ssh-keygen -f /etc/ssh/ssh_host_ed25519_key -N '' -t rsa -q -P ""
fi
if [ ! -f "/etc/ssh/ssh_host_dsa_key" ]; then
	# generate fresh dsa key
	ssh-keygen -f /etc/ssh/ssh_host_dsa_key -N '' -t dsa -q -P ""
	ssh-keygen -f /etc/ssh/ssh_host_ecdsa_key -N '' -t dsa -q -P ""
fi

#prepare run dir
if [ ! -d "/var/run/sshd" ]; then
  mkdir -p /var/run/sshd
fi

if [ -z "$SYSLOG_SERVER" ]
then
	echo 'SYSLOG_DISABLE'
else
	echo "*.* @$SYSLOG_SERVER:514" >> /etc/rsyslog.conf
fi

rsyslogd -i /tmp/rsyslog.pid -f /etc/rsyslog.conf

exec "$@"