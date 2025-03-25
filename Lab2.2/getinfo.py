from parse_logs import show_interfaces
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/configs')
def configs():
    return render_template('configs.html',hosts = list(d.keys()))

@app.route('/config/<hostname>')
def interfaces(hostname):
    return render_template('interfaces.html',hosts = hostname, interfaces = d[hostname])

if __name__ == '__main__':
    d = show_interfaces()
    app.run(debug=True)