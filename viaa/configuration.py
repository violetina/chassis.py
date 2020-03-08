import os
import sys
import yaml
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

    def __init__(self, config_from_env=False):
        self.config_from_env = config_from_env
        self.app_cfg={'module_name':os.path.split(
                    os.path.split(repr(__file__))[0])[-1]}
        cfg = {}
        if self.config_from_env:
            self.app_cfg=os.environ
            self.config["logging"] = {"level": 10}
        else:
           # config = {}
            
            # TODO: Take config from commandline arguments
            # TODO: Take config from environment variables
            # Take config from the user's config file
            if os.path.isfile(os.getcwd() + "/config.yml"):
                with open(os.getcwd() + "/config.yml", "r") as ymlfile:
                    cfg: dict = yaml.load(ymlfile, Loader=yaml.FullLoader)
            # Fallback to default
            else:
                cfg = {"viaa":{"logging": {"level": 10,"RabPub":{"host":"test","passw":"test","user":"test"}}}}
    
            if "viaa" in cfg:
                self.config = cfg["viaa"]
            if "application" in cfg:
                self.app_cfg =cfg["application"]
        
       # print(cfg)



