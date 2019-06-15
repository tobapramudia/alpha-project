import re,datetime

str_data = '<38>Jun 14 22:29:23 hello sshd: Connection closed by 127.0.0.1 port 50994 [preauth]';
raw_logs = str_data.split(None,5)
date_raw = datetime.datetime.now().strftime('%Y ') + str(re.sub(r'\<.+\>','',raw_logs[0]) + ' ' + raw_logs[1] + ' ' + raw_logs[2])
date = datetime.datetime.strptime(date_raw, '%Y %b %d %H:%M:%S')
hostname = raw_logs[3]
service = str(re.sub(r'\[.+\]?\:','',raw_logs[4])).split(':',1)[0]
print(service)

# print(raw_logs)
# print(date)
# print(parser)
# print()
# datetime.datetime.strptime(date, '%b %m %X')
# x_date = datetime.datetime.strptime(date, '%Y %b %d %H:%M:%S')