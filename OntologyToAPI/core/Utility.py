import importlib.util
import sys
import subprocess
import os
import logging
from pathlib import Path
from pydantic import BaseModel, create_model, ConfigDict
from typing import Any, List, Dict, Union
import rdflib
from Settings import auto_config as cfg

TYPE_MAP = {
    'float': float,
    'str': str,
    'int': int,
    'bool': bool,
    'object': dict,
    'list': list,
    'object_list': list
}

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


def build_nested_model(name: str, flat_data: Dict[str, Any]) -> type[BaseModel]:
    tree = {}
    for key, (rdf_type, _) in flat_data.items():
        parts = key.split('.')
        current = tree
        for i, part in enumerate(parts):
            if part not in current:
                current[part] = {"_children": {}}
            if i == len(parts) - 1:
                current[part]["_type"] = str(rdf_type)
            current = current[part]["_children"]

    def generate_pydantic(model_name: str, node_dict: Dict) -> type[BaseModel]:
        fields = {}
        for field_name, metadata in node_dict.items():
            field_type_str = metadata.get("_type", "object")
            children = metadata.get("_children")
            if children:
                sub_model = generate_pydantic(f"{field_name}Model", children)
                if field_type_str == 'object_list':
                    fields[field_name] = (List[sub_model], ...)
                else:
                    fields[field_name] = (sub_model, ...)
            else:
                python_type = TYPE_MAP.get(field_type_str, Any)
                fields[field_name] = (python_type, ...)
        return create_model(model_name, **fields, __config__=ConfigDict(extra='allow'))

    return generate_pydantic(name, tree)