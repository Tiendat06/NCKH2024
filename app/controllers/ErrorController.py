from flask import render_template
import traceback

class ErrorController:
    def __init__(self):
        pass

    # [GET]
    def index(self, error):
        # split_error = str(error).split(':')
        split_error = str(error).split(':')
        error_type = split_error[0] if len(split_error) > 0 else ""
        error_info = split_error[1] if len(split_error) > 1 else ""
        return render_template('error/error.html', error_type=error_type, error_info=error_info)