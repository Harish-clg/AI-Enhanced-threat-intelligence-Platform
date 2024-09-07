from flask import Flask, request, redirect, url_for
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = f"uploads/{file.filename}"
            file.save(file_path)
            subprocess.run(["python", "process_file.py", file_path])
            return 'File uploaded and processed successfully!'
    return '''
    <!doctype html>
    <title>Upload File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)
