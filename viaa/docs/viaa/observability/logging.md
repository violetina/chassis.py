# Logging

> Auto-generated documentation for [viaa.observability.logging](../../../viaa/observability/logging.py) module.

- [Chassis](../../README.md#viaa-chassis) / [Modules](../../MODULES.md#chassis-modules) / [Viaa](../index.md#viaa) / [Observability](index.md#observability) / Logging
    - [get_logger](#get_logger)

## get_logger

[[find in source code]](../../../viaa/observability/logging.py#L22)

```python
def get_logger(name='', config: ConfigParser = None):
```

Return a logger with the specified name and configuration, creating it if necessary.
If no name is specified, return the root logger.
If a config is specified it will override the current config for a logger.

#### See also

- [ConfigParser](../configuration.md#configparser)
