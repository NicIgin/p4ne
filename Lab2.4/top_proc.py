import requests
from flask import Flask, render_template

host_ip = '10.31.70.209'
login = 'restapi'
password = 'j0sg1280-7@'
api_url = '/restconf/data/Cisco-IOS-XE-process-memory-oper:memory-usage-processes'

headers = {
    "accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
def get_proc():
    r = requests.get('https://' + host_ip + api_url, auth=(login, password), headers=headers, verify=False)
    list_proc = []
    for ps in r.json()['Cisco-IOS-XE-process-memory-oper:memory-usage-processes']['memory-usage-process']:
        if 'holding-memory' in ps:
            list_proc.append((ps['name'],ps['holding-memory']))

    def key_value(proc):
        return proc[1]

    sorted_list = sorted(list_proc,key=key_value, reverse=True)
    top10_proc = []
    for i in range(0,10):
        top10_proc.append(sorted_list[i])
    return top10_proc

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/top_proc')
def top_proc():
    return render_template('top_proc.html', procs=get_proc())

if __name__ == '__main__':
    app.run(debug=True)
