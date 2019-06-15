from flask import Flask,request,g,render_template,jsonify
import os,json,sqlite3
from time import strftime

app_dir = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(app_dir, "app.db")
cache_file = os.path.join(app_dir, "cache.json")

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES )
    g._database.row_factory = sqlite3.Row
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def is_json(raw_stdin):
  try:
    json_object = json.loads(raw_stdin)
  except ValueError, e:
    return False
  return True

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def r_index():
	ssh_q = """
	select ifnull(count(l.id),0) as count_log,l.* FROM logs as l left join services as s on l.service_id=s.id where s.name LIKE'ssh%' group  by l.service_id,hostname
	"""
	x_ssh = query_db(ssh_q)
	ssh = []
	try:
		for x in x_ssh:
			ssh += [{'row': x}]
	except Exception as e:
		pass
	finally:
		pass
	data = {
		'title' : 'Welcome',
		'ssh_fails': ssh
	}
	return render_template('index.j2', data=data)

@app.route('/reports')
def r_report():
	data = {
		'data': 'data'
	}
	return render_template('reports.j2', data=data)

@app.route('/reports/ajax')
def r_report_ajax():
	page = 0 if request.args.get('page') == None  else request.args.get('page')
	limit = 50 if request.args.get('limit') == None  else request.args.get('limit')
	start = 0 if request.args.get('start') == None  else request.args.get('start')
	skip = int(page) * int(limit)
	q_data = '''
	select s.name as service, l.* from logs as l
	left join services as s on l.service_id=s.id
	order by id desc
	limit %s,%s
	''' % (str(skip),str(limit))
	res_data = list();
	c_row = 0

	for row in query_db(q_data):
		c_row += 1
		res_data += [{
			'id': row['id'],
			'service': row['service'],
			'ip_addr': row['ip_addr'],
			'hostname': row['hostname'],
			'date_server': row['date_server'],
			'raw_log': row['raw_log'],
		}]
	data = {
		'data': res_data,
		'success': True,
		'totalCount': query_db('select ifnull(count(id),0) as total from logs')[0][0]
	}
	return jsonify(data)

@app.route("/syslog", methods=['GET', 'POST'] )
def r_syslog():
	data = request.stream.read()
	if is_json(data):
		json_data = json.loads(data)
		v_key = set(['date','hostname','ip_addr','log','service'])
		if v_key.issubset(json_data.keys()):
			db = get_db()
			cur = db.cursor()
			service = query_db("select * from services where name = ?",[json_data['service']], one=True)			
			if service is None:
				s_name = json_data['service']
				cur.execute("INSERT INTO services(`name`) values (?)", [s_name])
				db.commit()
				service_id = cur.lastrowid
			else:
				service_id = service[0]
			cur.execute("INSERT INTO logs(`ip_addr`,`hostname`,`date_server`,`service_id`,`raw_log`,`created_at`) VALUES (?, ?, ?, ?, ?, ?)", [ json_data['ip_addr'],json_data['hostname'],json_data['date'],service_id,json_data['log'],strftime("%Y-%m-%d %H:%M:%S") ])
			db.commit()
		db.close()
	return 'ok'