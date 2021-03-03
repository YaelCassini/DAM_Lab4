from flask import Flask, request
from flask import render_template
import os
from PIL import Image
import watermark


app = Flask(__name__)


# 主页
@app.route('/', methods=['GET', 'POST'], strict_slashes=False)
def home():
    return render_template('home.html')


# 显示水印结果
@app.route('/upload', methods=['POST'], strict_slashes=False)
def Watermark():
    pic_addr=request.files['pic_addr']
    pic_path="./static/images/"+pic_addr.filename
    name, category = os.path.splitext(pic_addr.filename)  # 分解文件扩展名
    marked_path = "./static/images/" + name+"_marked.png"
    decode_path = "./static/images/" + name + "_decode.png"
    mark_addr=request.files['mark_addr']
    mark_path="./static/images/"+mark_addr.filename
    img_mark = Image.open(mark_path).convert("RGB")
    mark_path = "./static/images/" + name + "_mark.png"
    img_mark.save(mark_path)
    watermark.addWaterMark(pic_path, mark_path, marked_path)
    watermark.testWaterMark(marked_path, mark_path, decode_path)

    return render_template('watermark.html', pic_addr=pic_path, mark_addr=mark_path, marked_addr=marked_path, decode_addr=decode_path)


if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)