from flask import Flask
from demo import ANSWER
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Flask Dockerized'

@app.route('/demo')
def demo():
    return ANSWER

@app.route('/health')
def health():
    return 'healthy'

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0',port=8080)

