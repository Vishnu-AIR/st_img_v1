from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_uploads import UploadSet, configure_uploads, IMAGES
from datetime import datetime
from ultralytics import YOLO

app = Flask(__name__)

# Configure the image upload settings
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'
configure_uploads(app, photos)

model = YOLO("best (2).pt")

@app.route('/')
def index():
    return render_template('index.html')

def predict(image):
    try:
   
        results = model.predict(source="uploads/"+image)

        # Process the results and create a response
        l = []
        names = {0: 'blackheads', 1: 'dark spot', 2: 'nodules', 3: 'papules', 4: 'pustules', 5: 'whiteheads'}

        for idx, result in enumerate(results[0].boxes.xyxy):
            l.append(names[results[0].boxes.cls[idx].item()])

        d = {}
        for key, value in names.items():
            d[value] = l.count(value)

        response_data = {
            'predictions': d,
            'message': 'Prediction successful'
        }

        print(response_data)
        #print("hi")
        return response_data

    except Exception as e:
        #print("__ERROR__ ")
        return  str(e)


@app.route('/upload', methods=['POST'])
def upload():
    if 'photo' in request.files:
        photo = request.files['photo']
        if photo.filename != '':
            photo.filename = str(datetime.now()) + ".jpg"
            filename = photos.save(photo)
            tofa = predict(filename)
            return jsonify({"data": tofa})
    return 'No file selected for upload.'

if __name__ == '__main__':
    app.run(debug=False)

