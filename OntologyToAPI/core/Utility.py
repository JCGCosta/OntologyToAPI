import importlib.util
import sys
import subprocess
import os
import logging
from pathlib import Path
from Settings import auto_config as cfg

def handle_upload_file(uploaded_file):
    UPLOAD_DIR = Path(cfg.UPLOAD_DIR)
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    file_path = os.path.join(UPLOAD_DIR, uploaded_file.filename)

    with open(file_path, "wb") as out_file:
        while chunk := uploaded_file.file.read(1024 * 1024):  # Read in 1 MiB chunks
            out_file.write(chunk)
        out_file.close()

    uploaded_file.file.close()

    return file_path

def import_function_from_file(filepath, function_name):
    # Check if file exists
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    module_name = os.path.splitext(os.path.basename(filepath))[0]

    try:
        spec = importlib.util.spec_from_file_location(module_name, filepath)
        if spec is None:
            raise ImportError(f"Could not load module spec from {filepath}")

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
    except Exception as e:
        raise ImportError(f"Failed to load module '{module_name}': {e}")

    # Check if function exists
    if not hasattr(module, function_name):
        raise AttributeError(f"Function '{function_name}' not found in '{filepath}'")

    func = getattr(module, function_name)
    if not callable(func):
        raise TypeError(f"'{function_name}' in '{filepath}' is not a callable function")

    return func

def install_package(package_name):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        logging.info(f"Package '{package_name}' installed successfully.")
    except subprocess.CalledProcessError as e:
        logging.info(f"Failed to install '{package_name}': {e}")

def ensure_package_installed(package_name):
    if importlib.util.find_spec(package_name) is None:
        install_package(package_name)
    else:
        logging.info(f"Package '{package_name}' is already installed.")