# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from pyzbar.pyzbar import decode
import cv2
import subprocess
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'CXK'  # 添加一个密钥，用于 Flash 消息
print("++++++++++++++++++++++++++++++++++++++++++++++++++\n")
print("++++++++++++++++++++++++++++++++++++++++++++++++++\n")
print("++++++++++++++++++++++++++++++++++++++++++++++++++\n")
light_blue = "\033[38;2;0;173;239m"
reset_color = "\033[0m"
print(f"{light_blue}Made by NEUQ_Thunder_Wang{reset_color}") 
print("++++++++++++++++++++++++++++++++++++++++++++++++++\n")
print("++++++++++++++++++++++++++++++++++++++++++++++++++\n")
result = subprocess.run(['ipconfig'], capture_output=True, text=True)
# 使用正则表达式查找无线局域网适配器 WLAN 的 IPv4 地址
match = re.search(r'无线局域网适配器 WLAN.*?IPv4 地址[^\r\n:]+:\s*([^\s]+)', result.stdout, re.DOTALL | re.IGNORECASE)
if match:
    print("++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    wireless_ipv4_address = match.group(1)
    light_blue = "\033[38;2;0;173;239m"
    reset_color = "\033[0m"
    print(f"{light_blue}手机上直接搜 http://{wireless_ipv4_address}{reset_color}")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++\n")
# 模拟的葡萄生长周期数据
grape_data = {
    'uid1': {'1': 'static/images/uid1_01.jpg', '2': 'static/images/uid1_02.jpg', '3': 'static/images/uid1_03.jpg'},
    'uid2': {'1': 'static/images/pic_01.jpg', '2': 'static/images/pic_01.jpg', '3': 'static/images/pic_01.jpg'},
    # 添加更多 UID 和对应的生长周期图片链接
}

def read_qr_code(image_path):
    print("Inside read_qr_code function")
    print("Image Path:", image_path)

    image = cv2.imread(image_path)
    print("Image Read Result:", image is not None)

    qr_codes = decode(image)
    print("QR Codes:", qr_codes)

    if qr_codes:
        return qr_codes[0].data.decode('utf-8')
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/grape_search', methods=['GET', 'POST'])
def grape_search():
    success_message = None
    error_message = None
    uid = ''  # 设置 uid 的默认值为空字符串

    if request.method == 'POST':
        uid = request.form.get('uid', '')

        if 'photo' in request.files:
            uploaded_photo = request.files['photo']
            if uploaded_photo:
                filename = f"uploads/uploaded_{secure_filename(uploaded_photo.filename)}"
                uploaded_photo.save(filename)

                # 判断是否来自相机拍照
                if 'camera' in request.user_agent.string:
                    uid_from_qr = read_qr_code(filename)
                    if uid_from_qr:
                        uid = uid_from_qr
                        success_message = f'Successfully identified UID: {uid}'
                else:
                    # 处理通过文件上传的情况
                    uid_from_qr = read_qr_code(filename)
                    if uid_from_qr:
                        uid = uid_from_qr
                        success_message = f'Successfully identified UID from uploaded file: {uid}'

        selected_uid_data = grape_data.get(uid, {})

        if not selected_uid_data:
            error_message = 'Please check the UID.'
            flash(error_message, 'error')
            return render_template('grape_search.html', uid=uid, photos={}, error_message=error_message, success_message=success_message)

        return render_template('grape_photos.html', uid=uid, photos=selected_uid_data, success_message=success_message)

    return render_template('grape_search.html', uid=uid, photos={}, error_message=error_message, success_message=success_message)

@app.route('/grape_photos/<uid>')
def grape_photos(uid):
    selected_uid_data = grape_data.get(uid, {})
    return render_template('grape_photos.html', uid=uid, photos=selected_uid_data)

@app.route('/vineyard_experience')
def vineyard_experience():
    return render_template('vineyard_experience.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)
    # host_ip = get_host_info()
    # print(f"Host IP Address: {host_ip}")
    