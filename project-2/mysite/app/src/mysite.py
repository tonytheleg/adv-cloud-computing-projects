from flask import Flask, render_template, send_file, current_app as app

app = Flask(__name__)

@app.route('/')
def serve_site():
    return render_template('index.html')

@app.route('/healthcheck')
def check_health():
    return "SITE IS UP"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
