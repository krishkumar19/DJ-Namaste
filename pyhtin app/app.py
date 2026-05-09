from flask import Flask, send_from_directory, request, redirect, url_for
import os
import sqlite3

# Initialize Flask app, pointing the static and template folder to "DJ Namasta"
current_dir = os.path.dirname(os.path.abspath(__file__))
website_dir = os.path.join(current_dir, "DJ Namasta")

app = Flask(__name__, static_folder=website_dir, static_url_path='')

def get_db_connection():
    conn = sqlite3.connect(os.path.join(current_dir, 'database.db'))
    conn.row_factory = sqlite3.Row
    return conn

# Route to serve the main index.html
@app.route('/')
def home():
    return send_from_directory(website_dir, 'index.html')

# Route to serve any other HTML pages (like contact.html, about.html)
@app.route('/<path:path>')
def serve_html(path):
    return send_from_directory(website_dir, path)

# Route to handle form submissions
@app.route('/submit_request', methods=['POST'])
def submit_request():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject', '')
    message = request.form.get('message', '')
    
    # We will map this to our service_requests table
    # employe_id is auto-incremented
    # We can split name into first and last name roughly
    parts = name.split(maxsplit=1)
    first_name = parts[0] if parts else ""
    last_name = parts[1] if len(parts) > 1 else ""
    
    # For simplicity, we store the subject/message in state/city fields 
    # (Since this is what the desktop app currently displays)
    state = subject[:50]
    city = message[:50]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO service_requests (first_name, last_name, email_address, state, city)
        VALUES (?, ?, ?, ?, ?)
    ''', (first_name, last_name, email, state, city))
    conn.commit()
    conn.close()

    # Redirect back to a thank you page or the contact page
    return redirect('/contact.html?success=1')

if __name__ == '__main__':
    print(f"Starting Flask server serving from: {website_dir}")
    app.run(debug=True, port=5000)
