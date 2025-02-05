import os
from flask import Flask, flash, request, redirect, url_for,render_template
from flask import send_from_directory
from werkzeug.utils import secure_filename
import predictions
import get_poke_facts
import settings

UPLOAD_FOLDER = settings.settings['UPLOAD_PATH']
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            predicts = predictions.predict(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            facts = get_poke_facts.get_facts(predicts[0])
            print(facts)
            return render_template("pokemon.html", facts=facts, pokemon_name=predicts[0] , image_data=predicts[1], pokemon_percentage=predicts[2], image_pokemon = predicts[3])
            #return 'Jeg tror det er en: {}'.format(str(predicts[0]))
    return render_template("upload.html",)




@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


app.run(threaded=False)
