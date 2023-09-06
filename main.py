from flask import Flask, render_template, request, flash
import os
import cv2 
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'webp', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set your secret key for flash messages
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename, operation):
    print(f"The operation is {operation} and filename is {filename}")
    img=cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            imgProcessed=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            newfilename=f"static/{filename}"
            cv2.imwrite( newfilename,imgProcessed)
            return newfilename
        case "cwebp":
            newfilename=f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newfilename,img)
            return newfilename
        case "cjpg":
            newfilename=f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newfilename,img)
            return newfilename
        case "cpng":
            newfilename=f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newfilename,img)
            return newfilename
        case "cjpeg":
            newfilename=f"static/{filename.split('.')[0]}.jpeg"
            cv2.imwrite(newfilename,img)
            return newfilename
        case "cpdf":
            newfilename=f"static/{filename.split('.')[0]}.pdf"
            cv2.imwrite(newfilename,img)
            return newfilename
        case "cpdf":
            newfilename=f"static/{filename.split('.')[0]}.jpeg"
            cv2.imwrite(newfilename,img)
            return newfilename
    pass 
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/use')
def use():
    return render_template("use.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/edit', methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        operation = request.form.get("operation")
        if 'file' not in request.files:
            flash('No file part', 'error')
            return "error: No file part"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file', 'error')
            return "error: No selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new=processImage(filename, operation)
            flash(f"Your Image is Processed and is Available <a href='/{new}'target='_blank'>Here</a>", 'success')
            return render_template("index.html")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)