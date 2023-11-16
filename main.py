import http.server
import socketserver
import random
import yaml

class QuoteHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Content-Security-Policy', "default-src 'self'")
        http.server.SimpleHTTPRequestHandler.end_headers(self)

    def guess_type(self, path):
        if path.endswith(".html"):
            return 'text/html; charset=utf-8'
        elif path.endswith(".css"):
            return 'text/css'
        else:
            return http.server.SimpleHTTPRequestHandler.guess_type(self, path)

    def get_random_quote(self):
        with open('quotes.yaml', 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            quotes = data['quotes']
            return random.choice(quotes)

    def generate_html_with_quote(self):
        random_quote = self.get_random_quote()
        with open('quotes.html', 'r', encoding='utf-8') as file:
            html_template = file.read()
            return html_template.replace('{quote}', random_quote)

    def do_GET(self):
        if self.path != '/style.css':
            self.path = '/quotes.html'
            
        self.send_response(200)
        self.send_header('Content-type', self.guess_type(self.path))
        self.end_headers()

        if self.path == '/quotes.html':
            html_with_quote = self.generate_html_with_quote()
            self.wfile.write(html_with_quote.encode('utf-8'))
        elif self.path == '/style.css':
            with open('style.css', 'rb') as file:
                self.wfile.write(file.read())
        else:
            http.server.SimpleHTTPRequestHandler.do_GET(self)

# Set up the server
PORT = 8080
handler = QuoteHandler
handler.extensions_map.update({'.css': 'text/css'})
with socketserver.TCPServer(("", PORT), handler) as httpd:
    print("Server started at port", PORT)
    httpd.serve_forever()