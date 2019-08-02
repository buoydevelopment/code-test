from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
  return 'Hello World'

app.run(port=5050)

# __name__ = "__main__"