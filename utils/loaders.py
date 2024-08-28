import yaml

def load_config(config_file:str):
    # Load configs
    with open(config_file, 'r') as stream:
        config = yaml.safe_load(stream)
    return config
