# Configuration

> Auto-generated documentation for [viaa.configuration](../../viaa/configuration.py) module.

- [Chassis](../README.md#viaa-chassis) / [Modules](../MODULES.md#chassis-modules) / [Viaa](index.md#viaa) / Configuration
    - [ConfigParser](#configparser)

## ConfigParser

[[find in source code]](../../viaa/configuration.py#L4)

```python
class ConfigParser():
    def __init__(config_from_env=False):
```

The ConfigParser has a config dictionary containing
all the configuration for the Chassis, but it can also be
used for program-specific configuration.
The configuration can come from multiple sources and if
duplicate settings are found the one from the source with
the highest priority will be used.
1. Commandline arguments
2. Environment variables
3. Config file
4. Defaults
