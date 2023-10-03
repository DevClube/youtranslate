

from flask import Flask, request, send_file
import os
from test import translate_srt, read_srt, write_srt, remove_file
from flask_cors import CORS
import io

app = Flask(__name__)
CORS(app)

# @app.route("/", methods=["GET"])
# def index():
#     return render_template("index.html")
# # Define a route to handle file uploads



@app.route('/upload', methods=['POST'])
def upload():
    try:
        # Get the uploaded file.
        file = request.files['file']
        original_file_name = os.path.splitext(file.filename)[0]

        # Read the SRT content from the file.
        srt_content = file.read().decode('utf-8')

        # Translate the SRT content.
        translated_content = translate_srt(srt_content, request.args.get('dest_language'))

        # Create an in-memory byte stream.
        output = io.BytesIO()
        output.write(translated_content.encode('utf-8'))
        output.seek(0)

        # Send the translated file back as a response object.
        return send_file(
            output,
            as_attachment=True,
            download_name=f'{original_file_name}_{request.args.get("dest_language")}.srt',
            mimetype='text/plain'
        )

    except Exception as e:
        return f"An error occurred: {e}"



if __name__ == '__main__':
    app.run(debug=True)