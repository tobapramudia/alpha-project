import SocketServer
import re,datetime
import json,urllib2,argparse,time

HOST, PORT = "0.0.0.0", 514
parser = argparse.ArgumentParser(description='help')
parser.add_argument('--server', help='Port for servers', default='http://127.0.0.1:5000', required=False)
args = parser.parse_args()

class SyslogUDPHandler(SocketServer.BaseRequestHandler):

	def handle(self):
		socket = self.request[1]
		ip_addr = self.client_address[0]
		raw_tcp = bytes.decode(self.request[0])

		raw_logs = raw_tcp.split(None,5)
		try:
			date_raw = datetime.datetime.now().strftime('%Y ') + str(re.sub(r'\<.+\>','',raw_logs[0]) + ' ' + raw_logs[1] + ' ' + raw_logs[2])
			date = datetime.datetime.strptime(date_raw, '%Y %b %d %H:%M:%S')
			service = str(re.sub(r'\[.+\]?\:','',raw_logs[4])).split(':',1)[0]
			hostname = raw_logs[3]

			data = {
				'ip_addr': ip_addr,
				'date': str(date),
				'hostname': hostname,
				'service': service,
				'log': raw_logs[5]
			}
			url_path = args.server + '/syslog'
			req = urllib2.Request(url_path)
			req.add_header('Content-Type', 'application/json')
			res = urllib2.urlopen(req, json.dumps(data))
		except Exception as e:
			pass
		finally:
			pass

if __name__ == "__main__":
	try:
		print('Initial Server' + args.server)
		server = SocketServer.UDPServer((HOST,PORT), SyslogUDPHandler)
		server.serve_forever(poll_interval=10)
	except (IOError, SystemExit):
		raise e
	except KeyboardInterrupt:
		print ("Crtl+C Pressed. Shutting down.")