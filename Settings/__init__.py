import os

class Env:
    UPLOAD_DIR = os.getenv('UPLOAD_DIR', "tmp/uploads")
auto_config = Env