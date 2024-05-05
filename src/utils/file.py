import numpy as np
import yaml
import os
import dill


def read_yaml_file(path: str) -> dict:
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def write_yaml_file(path: str, content: object, replace: bool = False) -> None:
    if replace:
        if os.path.exists(path):
            os.remove(path)
    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        yaml.dump(content, f)

def read_npy_file(path: str) -> np.array:
    with open(path, 'rb') as f:
        return np.load(f)

def write_npy_file(path: str, content: object, replace: bool = False) -> None:
    if replace:
        if os.path.exists(path):
            os.remove(path)
    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    np.save(path, content)

def save_obj_file(path: str, content: object, replace: bool = False) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'wb') as f:
        dill.dump(content, f)
