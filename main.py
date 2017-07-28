from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello, World!'

@app.route('/hello')
def hello():
  return render_template('addword.html')

@app.route('/hello/<num>')
def hello_num(num):
  return render_template('addword.html', num=int(num))

# @app.route('/hello/<user>')
# def hello_name(user):
#    return render_template('hello.html', name = user)


if (__name__=="__main__"):
  app.run()

