"""
八下道法抽测系统 - 后端服务
端口: 1101
功能: 保存/加载答题记录、评分历史
"""
import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {'progress': {}, 'scores': []}
    return {'progress': {}, 'scores': []}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

class Handler(BaseHTTPRequestHandler):
    def _send(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def do_OPTIONS(self):
        self._send({'ok': True})

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip('/')
        
        if path == '/api/progress':
            data = load_data()
            self._send({'ok': True, 'progress': data.get('progress', {})})
        elif path == '/api/records':
            data = load_data()
            self._send({'ok': True, 'records': data.get('records', [])})
        elif path == '/api/scores':
            data = load_data()
            self._send({'ok': True, 'scores': data.get('scores', [])})
        else:
            self._send({'error': 'not found'}, 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip('/')
        
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length else b'{}'
        
        try:
            req = json.loads(body)
        except:
            req = {}

        data = load_data()

        if path == '/api/progress':
            progress = req.get('progress', {})
            data['progress'] = progress
            save_data(data)
            self._send({'ok': True})

        elif path == '/api/record':
            record = req.get('record', {})
            if 'records' not in data:
                data['records'] = []
            data['records'].append(record)
            save_data(data)
            self._send({'ok': True})

        elif path == '/api/records':
            records = req.get('records', [])
            data['records'] = records
            save_data(data)
            self._send({'ok': True})

        elif path == '/api/scores':
            score = req.get('score', {})
            if 'scores' not in data:
                data['scores'] = []
            data['scores'].append(score)
            save_data(data)
            self._send({'ok': True, 'index': len(data['scores']) - 1})

        else:
            self._send({'error': 'not found'}, 404)

if __name__ == '__main__':
    port = 1101
    print(f'🚀 道法抽测系统后端启动 http://localhost:{port}')
    print(f'📁 数据文件: {DATA_FILE}')
    server = HTTPServer(('0.0.0.0', port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n服务已停止')
        server.server_close()