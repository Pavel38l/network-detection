import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    UPLOADED_IMAGES_DEST = 'static/images'
    OUTPUT_IMAGES_DEST = 'static/outputs'
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])