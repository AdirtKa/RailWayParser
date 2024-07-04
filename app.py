from flask import Flask, render_template_string
from main import main

app: Flask = Flask(__name__)
display: str = main().to_html()


@app.route('/')
def render():
    return render_template_string(display, h1='DataFrame')


if __name__ == '__main__':
    app.run()
