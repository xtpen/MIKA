from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from difflib import SequenceMatcher

# Define the dataset with keywords and corresponding responses
dataset = [
    (["fever"], "Apply a cold compress and take fever-reducing medication like paracetamol.", "mica.png"),
    (["headache"], "Rest in a quiet, dark room and take over-the-counter pain relievers like ibuprofen.", "headache_image.png"),
    # Add more responses and image paths as needed
]

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/image.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('image.html', 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_error(404, 'File Not Found')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        message = data['message']
        response_data = generate_response(message)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        self.wfile.write(json.dumps(response_data).encode())

def generate_response(message):
    # Check if the message matches any response in the dataset
    for keywords, response, image_path in dataset:
        if any(keyword in message.lower() for keyword in keywords):
            return {
                'response': response,
                'chathead': image_path
            }
    
    # If no match is found, provide a default response and image path
    default_response = "I'm sorry, I couldn't understand your message."
    default_image_path = "default_image.png"
    return {
        'response': default_response,
        'chathead': default_image_path
    }

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
