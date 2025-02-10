import sys
import subprocess
import socket
import webbrowser
import re
result = subprocess.run(['ipconfig'], capture_output=True, text=True)

# 使用正则表达式查找无线局域网适配器 WLAN 的 IPv4 地址
match = re.search(r'无线局域网适配器 WLAN.*?IPv4 地址[^\r\n:]+:\s*([^\s]+)', result.stdout, re.DOTALL | re.IGNORECASE)

if match:
    wireless_ipv4_address = match.group(1)
    print(f"Wireless LAN adapter Wi-Fi IPv4 Address: {wireless_ipv4_address}")
else:
    print("Unable to find Wireless LAN adapter Wi-Fi IPv4 Address.")
def install_libraries():
    try:
        subprocess.run([sys.executable, '-m','pip', 'install', 'Flask', 'Werkzeug', 'pyzbar', 'opencv-python'], check=True)
        print("Libraries installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing required libraries: {e}")
        exit(1)

def start_app():
    try:
        subprocess.Popen(['python', 'app.py'])
        print("App started successfully.")
    except Exception as e:
        print(f"Error starting app.py: {e}")
        exit(1)

def get_host_info():
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(socket.gethostname())
        print(f"Host Name: {host_name}")
    except Exception as e:
        print(f"Error getting host information: {e}")

def open_browser(host_ip):
    try:
        webbrowser.open_new_tab(f'http://127.0.0.1')
        print("Default browser opened successfully.")
    except Exception as e:
        print(f"Error opening browser: {e}")

if __name__ == "__main__":
    # 1. 安装所需库
    install_libraries()

    # 2. 启动 app.py 文件
    start_app()

    # 3. 记录电脑的 IP 地址
    host_ip = get_host_info()

    # 4. 打开默认浏览器并访问应用程序地址
    open_browser(host_ip)

    # 保持脚本运行，以便用户查看输出
    input("Press Enter to exit...")
