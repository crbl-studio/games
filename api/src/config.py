import tomli

config = None

with open('./config.toml', mode="rb") as config_file:
    config = tomli.load(config_file)
