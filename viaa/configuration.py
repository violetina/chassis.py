import os
import re
import sys
import yaml

tag = '!ENV'
pattern = re.compile('.*?\${(\w+)}.*?')


def constructor_env_variables(loader, node):
        """
        see https://medium.com/swlh/python-yaml-configuration-with-environment-variables-parsing-77930f4273ac
        Extracts the environment variable from the node's value
        :param yaml.Loader loader: the yaml loader
        :param node: the current node in the yaml
        :return: the parsed string that contains the value of the environment
        variable
        """
        value = loader.construct_scalar(node)
        match = pattern.findall(value)  # to find all env variables in line
        if match:
            full_value = value
            for g in match:
                full_value = full_value.replace(
                    f'${{{g}}}', os.environ.get(g, g)
                )
            return full_value
        return value

loader = yaml.SafeLoader
loader.add_constructor(tag, constructor_env_variables)



class ConfigParser():
    """The ConfigParser has a config dictionary containing
    all the configuration for the Chassis, but it can also be
    used for program-specific configuration.
    The configuration can come from multiple sources and if
    duplicate settings are found the one from the source with
    the highest priority will be used.
    1. Commandline arguments
    2. Environment variables
    3. Config file
    4. Defaults
    """
    path = sys.path.append(os.getcwd())

    config = {}

    def __init__(self):
        self.app_cfg={'module_name':os.path.split(
                    os.path.split(repr(__file__))[0])[-1]}
        cfg = {}
        
        # TODO: Take config from commandline arguments
        # TODO: Take config from environment variables
        # Take config from the user's config file
        if os.path.isfile(os.getcwd() + "/config.yml"):
            with open(os.getcwd() + "/config.yml", "r") as ymlfile:
                cfg: dict = yaml.load(ymlfile, Loader=loader)
        # Fallback to default
        else:
            cfg = {"viaa":{"logging": {"level": 10,"RabPub":{"host":"test","passw":"test","user":"test"}}}}
        if "viaa" in cfg:
            self.config = cfg["viaa"]
        if "application" in cfg:
            self.app_cfg =cfg["application"]

