#!/bin/sh
sleep 4
ssh-keyscan $1
while (sleep 0.5); do
	ssh -oBatchMode=yes -l root $1 echo 123
done