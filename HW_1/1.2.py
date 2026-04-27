from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello, Flask!'


@app.route('/user/<name>/')
def show_user_profile(name):
    return f'Так держать, {name}'


if __name__ == '__main__':
    app.run(debug=True)