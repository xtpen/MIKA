import pyttsx3

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Example usage:
text_to_speech("Welcome to MICA!")






# from flask import Flask, render_template

# app = Flask(__name__)

# # Route for registration page
# @app.route('/register')
# def register():
#     return render_template('register.html')

# # Route for login page
# @app.route('/login')
# def login():
#     return render_template('login.html')

# # Route for home page
# @app.route('/home')
# def home():
#     return render_template('home.html')

# if __name__ == '__main__':
#     app.run(debug=True)

