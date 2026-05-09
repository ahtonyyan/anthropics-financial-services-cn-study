#!/usr/bin/env python3
"""
金融技能学习网站 - 本地测试服务器
用法: python3 server.py
然后在浏览器访问: http://localhost:8000
"""

import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 启用CORS，避免本地开发跨域问题
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

def start_server():
    # 切换到网站目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    handler = MyHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"""
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║        📊 金融技能学习网站 - 本地测试服务器                  ║
║                                                            ║
║        服务器地址: http://localhost:{PORT}                   ║
║                                                            ║
║        按 Ctrl+C 停止服务器                                 ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
        """)

        # 自动打开浏览器
        try:
            webbrowser.open(f'http://localhost:{PORT}')
        except:
            pass  # 如果无法打开浏览器，继续运行服务器

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n服务器已停止。")
            sys.exit(0)

if __name__ == "__main__":
    start_server()
