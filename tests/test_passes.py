
import yaml

def load_config(config_path="config/config.yaml"):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
        return config

def test_python_working():
    assert 1 + 1 == 2

def test_config_loads():
    config = load_config()
    assert isinstance(config, dict)