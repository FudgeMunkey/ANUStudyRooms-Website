from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    text = open("static/data/scan.json", "r")
    my_content = text.read()
    text.close()
    return render_template('home.html', text=my_content)


if __name__ == '__main__':
    app.run()
