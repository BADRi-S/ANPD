from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import subprocess

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Directory to store uploaded files

# Define username and password
valid_username = 'Admin'
valid_password = '1234'

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/index', methods=['POST'])
def index():
    username = request.form['username']
    password = request.form['password']

    if username == valid_username and password == valid_password:
        return render_template('index.html')
    else:
        flash('Invalid username and/or password')
        return redirect(url_for('login'))

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Run predict.py with the uploaded file as source
            command = f"python predict.py source=\"{file_path}\""  
            os.system(command)

            output_image = 'output_image_0.jpg'
            output_labels = 'output_labels.txt'
            image_path = os.path.join('result', output_image)
            number_plate_text = ''

            if os.path.exists(image_path):
                # Read number plate text from output_labels.txt
                with open(os.path.join('result', output_labels), 'r') as labels_file:
                    number_plate_text = ', '.join([line.strip() for line in labels_file.readlines() if line.strip()])
                
                return render_template('result.html', number_plate_text=number_plate_text, image_path=image_path)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
