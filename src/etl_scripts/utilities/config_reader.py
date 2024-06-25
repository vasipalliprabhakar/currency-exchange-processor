import yaml


SECTION = 'exchange_api'


def get_api_config(file_path):
    with open(file_path, "r") as yaml_file:
        config_data = yaml.load(yaml_file, Loader=yaml.FullLoader)
    return config_data.get(SECTION)
