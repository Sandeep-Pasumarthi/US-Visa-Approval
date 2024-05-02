import yaml
import os


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
