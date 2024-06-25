import yaml
from pathlib import Path

CONFIG_FILE_PATH = Path(__file__).parent.parent.parent.joinpath("resources/config.yaml")


def get_api_config_params():
    with open(CONFIG_FILE_PATH, "r") as yaml_file:
        config_data = yaml.load(yaml_file, Loader=yaml.FullLoader)
    print(config_data.get("exchange_api"))
    return config_data.get("exchange_api")
