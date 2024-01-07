from flask import render_template
import traceback

class ErrorController:
    def __init__(self):
        pass

    def index(self, error):
        split_error = str(error).split(': ')
        return render_template('error/error.html', error_type = split_error[0], error_info = split_error[1])