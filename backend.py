from flask import Flask, render_template, send_file
from ai_part import financial_analyst, generate_plan
import io
from PIL import Image
import matplotlib.pyplot as plt
from markdown_utils import convert_markdown_to_html

app = Flask(__name__)

@app.route('/')
def index():
    text = financial_analyst()
    text2=generate_plan()
    html_content1 = convert_markdown_to_html('content.md')
    html_content2 = convert_markdown_to_html('plans.md')
    return render_template('index.html', content1=html_content1, content2=html_content2)
    #return render_template('index.html', text=text)

@app.route('/image')
def image():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
    img_io = io.BytesIO()
    plt.savefig(img_io, format='png')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
