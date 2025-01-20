# Importing the necessary libraries
import re
import json
import base64
import keras
import numpy as np
from PIL import Image
from flask import Flask, render_template, request, jsonify
import joblib
import cv2
from io import BytesIO
from flask import jsonify

# Define our output classes for doodle classification
out_classes = ['apple', 'bee', 'birthday_cake', 'book', 'butterfly', 'candle', 'camera', 'car', 'cloud', 'coffee_cup', 'donut', 'eyeglasses', 'flower', 'house', 'ice_cream', 'ladder', 'laptop', 'leaf', 'light_bulb', 'moon', 'octopus', 'pencil', 'penguin', 'pineapple', 'rainbow', 'star', 'smiley_face', 'snowman', 'snowflake', 'strawberry', 'traffic_light', 'tree', 'tennis_racquet', 't-shirt', 'umbrella', 'watermelon']

# Initialize our flask app
app = Flask(__name__)

# Load the color emotion classification model
color_emotion_model = joblib.load('color_emotion_rf_categorized_detailed.pkl')

# Load model for doodle classification (from Keras)
doodle_model = keras.models.load_model("doodle_model_main.keras", compile=False)

# Load animal doodle classification model
animal_doodle_model = keras.models.load_model("animal_doodle_model_main.keras", compile=False)

# Define classes for the animal doodle model
animal_classes = ['bee', 'cat', 'duck', 'lion', 'monkey']


# Fun facts for each class
fun_facts = {
    'apple': "An apple tree can live up to 100 years.",
    'bee': "Bees have to collect nectar from two million flowers to make one pound of honey.",
    'birthday_cake': "The largest birthday cake ever made weighed over 128,000 pounds!",
    'book': "The longest novel ever written is 'In Search of Lost Time' by Marcel Proust.",
    'butterfly': "Butterflies taste with their feet!",
    'candle': "Candles have been used for over 5,000 years.",
    'camera': "The first photograph ever taken was in 1826 by Joseph Nicéphore Niépce.",
    'car': "The first car ever made was built by Karl Benz in 1885.",
    'cloud': "Clouds can weigh millions of pounds.",
    'coffee_cup': "Coffee is the second most traded commodity in the world, after oil.",
    'donut': "Americans eat about 10 billion donuts each year.",
    'eyeglasses': "The first eyeglasses were invented in Italy in the late 13th century.",
    'flower': "The world's largest flower is the Rafflesia arnoldii, which can grow up to 3 feet wide.",
    'house': "The world's most expensive house is worth $2 billion in London.",
    'ice_cream': "The average American eats about 20 pounds of ice cream every year.",
    'ladder': "The longest ladder in the world is 44 meters (144 feet) long.",
    'laptop': "The first laptop was introduced in 1981 by Osborne Computer Corporation.",
    'leaf': "There are about 60,000 species of trees in the world.",
    'light_bulb': "Thomas Edison invented the first practical light bulb in 1879.",
    'moon': "The moon is 1/4 the size of Earth.",
    'octopus': "Octopuses have three hearts and blue blood.",
    'pencil': "The average pencil can draw a line 35 miles long.",
    'penguin': "Penguins are found in only the Southern Hemisphere.",
    'pineapple': "Pineapples are not grown on trees, but on the ground in a shrub.",
    'rainbow': "A rainbow can appear only when the sun is shining and it is raining at the same time.",
    'star': "The largest star known is UY Scuti, which is over 1,700 times the size of the sun.",
    'smiley_face': "The first use of the smiley face was in 1963 in a promotional campaign for an insurance company.",
    'snowman': "The world's largest snowman was built in Maine, USA, and stood 122 feet tall.",
    'snowflake': "No two snowflakes are ever exactly alike.",
    'strawberry': "Strawberries are the only fruit that wear their seeds on the outside.",
    'traffic_light': "The first traffic light was installed in London in 1868.",
    'tree': "The oldest living tree is a bristlecone pine in California that is over 5,000 years old.",
    'tennis_racquet': "The first tennis racquet was made from wood, but modern racquets are made from carbon fiber.",
    't-shirt': "The first T-shirt was sold in 1939 as a part of a soldier’s uniform.",
    'umbrella': "The oldest umbrella dates back to ancient China, over 4,000 years ago.",
    'watermelon': "Watermelons are 92% water, making them very hydrating!"
}

# Fun facts for each class
animal_fun_facts = {
    'bee': "Bees have to collect nectar from two million flowers to make one pound of honey.",
    'cat': "Cats can make over 100 different sounds.",
    'duck': "Ducks have waterproof feathers and can sleep while floating on water.",
    'lion': "Lions are the only cats that live in groups called prides.",
    'monkey': "Monkeys use tools, such as sticks, to gather food."
}

# Example sound file paths
animal_sounds = {
    "cat": "/static/cat_sound.mp3",
    "lion": "/static/lion_sound.mp3",
    "bee": "/static/bee_sound.mp3",
    "monkey": "/static/monkey_sound.mp3",
    "duck": "/static/duck_sound.mp3"
}

# Decoding an image from base64 into raw representation
def convertImage(imgData1, filename='output.png'):
    imgstr = re.search(r'base64,(.*)', imgData1).group(1).encode()
    with open(filename, 'wb') as output:
        output.write(base64.b64decode(imgstr))


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/classifier')
def classifier():
    return render_template("doodle_classifier.html")

# Route for color emotion classification page
@app.route('/color-emotion-classifier')
def color_emotion_classifier():
    return render_template("color_emotion_classifier.html")

# Route for doodle classifier page
@app.route('/predict/', methods=['POST'])
def predict():
    try:
        imgData = request.get_json()['image']
        print("Image data received")  # Debug

        convertImage(imgData, 'doodle_output.png')  # Use unique filename for doodle classifier
        print("Image converted")  # Debug

        pil_img = Image.open('doodle_output.png').convert('L')
        # Resize to 32x32 as required by the model
        x = np.array(pil_img.resize((32, 32), resample=Image.LANCZOS))
        x = np.invert(x)
        x = x.reshape(1, 32, 32, 1)  # Reshape to match model's input dimensions (32x32, 1 channel)
        x = x / 255.0

        pred = doodle_model.predict(x)
        print("Prediction done:", pred)  # Debug

        ind = (-pred).argsort()[0][:3]
        predicted_class = out_classes[ind[0]]
        fun_fact = fun_facts.get(predicted_class, "No fun fact available.")  # Get the fun fact for the predicted class
        
        response = {
            'prediction': predicted_class,
            'fun_fact': fun_fact  # Include the fun fact in the response
        }

        print("Response:", response)  # Debug
        return json.dumps(response)

    except Exception as e:
        print("Error:", str(e))  # Print any error
        return json.dumps({"error": str(e)})


@app.route('/predict-color-emotion', methods=['POST'])
def predict_color_emotion():
    try:
        data = request.get_json()
        selected_color = data.get('color')

        color_to_emotion = {
            'red': 'Anger', 'blue': 'Calm', 'yellow': 'Happiness', 'green': 'Relaxed', 'purple': 'Creativity',
            'pink': 'Joyful', 'orange': 'Excitement', 'brown': 'Comfort', 'grey': 'Sadness', 'turquoise': 'Tranquility',
            'maroon': 'Passion', 'lime': 'Energy', 'lavender': 'Peace', '#00ffff': 'Serenity', 'beige': 'Warmth',
            'peach': 'Delight', 'gold': 'Wealth', 'silver': 'Sophistication', 'indigo': 'Mystery', 'violet': 'Elegance',
            'coral': 'Joyful', '#3eb489': 'Freshness', '#7cb9e8': 'Refreshing', '#36454f': 'Strength', 'fuchsia': 'Excitement',
            'chartreuse': 'Vibrancy'
        }

        emotion = color_to_emotion.get(selected_color, 'Unknown Emotion')
        return jsonify({'emotion': emotion})

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/animal-doodle')
def animal_doodle():
    return render_template("animal_doodle_classifier.html")


@app.route('/predict-animal', methods=['POST'])
def predict_animal():
    data = request.get_json()
    image_data = data.get('image')
    
    # Convert base64 image to a file
    convertImage(image_data, 'animal_output.png')
    
    # Read and process the image
    img = cv2.imread('animal_output.png')

    # Convert the image to grayscale (single channel)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Resize the image to 32x32 as required by the model
    img = cv2.resize(img, (32, 32))

    # Expand dimensions to match model input shape (1, 32, 32, 1) for grayscale
    img = np.expand_dims(img, axis=-1)  # Add channel dimension (1 for grayscale)
    img = np.expand_dims(img, axis=0)   # Add batch dimension

    # Normalize the image
    img = img / 255.0
    
    # Predict using the animal doodle model
    pred = animal_doodle_model.predict(img)  # Pass the correctly shaped image

    # Get predicted class and fun fact
    predicted_class = animal_classes[np.argmax(pred)]
    fun_fact = animal_fun_facts.get(predicted_class, "No fun fact available.")
    animal_sound = animal_sounds.get(predicted_class, None)

    return jsonify({
        'prediction': predicted_class,
        'fun_fact': fun_fact,
        'sound': animal_sound
    })

if __name__ == '__main__':
    app.run(debug=True)
