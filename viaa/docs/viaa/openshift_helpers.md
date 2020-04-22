# Openshift Helpers

> Auto-generated documentation for [viaa.openshift_helpers](../../viaa/openshift_helpers.py) module.

Created on Fri Jan 31 11:24:17 2020

- [Chassis](../README.md#viaa-chassis) / [Modules](../MODULES.md#chassis-modules) / [Viaa](index.md#viaa) / Openshift Helpers
    - [ConfigFromOpenshift](#configfromopenshift)
        - [ConfigFromOpenshift().get_cfg](#configfromopenshiftget_cfg)
        - [ConfigFromOpenshift().get_cfg_dct](#configfromopenshiftget_cfg_dct)
        - [ConfigFromOpenshift().update_local_cfg](#configfromopenshiftupdate_local_cfg)
        - [ConfigFromOpenshift().update_oc_cfg](#configfromopenshiftupdate_oc_cfg)
    - [CreatePipeline](#createpipeline)
    - [CreateTemplate](#createtemplate)

@author: tina

## ConfigFromOpenshift

[[find in source code]](../../viaa/openshift_helpers.py#L311)

```python
class ConfigFromOpenshift():
    def __init__(
        app,
        host,
        token=None,
        interactive=False,
        config_file=None,
        yamlfile=None,
    ):
```

    - viaa python chassis config from openshift secret
### Aargs

- app:
     - appliction name
- host:
    - the openshift api uri
- oc token:
    - oc whoami -t
- interactive:
    - bool , if true asks for above args
- config_file:
    - the name of the config file if update_local_cfg methode is called

- yamlfile:
    - the name of the yaml file to use for upload to openshift secret

### ConfigFromOpenshift().get_cfg

[[find in source code]](../../viaa/openshift_helpers.py#L359)

```python
def get_cfg():
```

- Get the config from secret, yaml as string
- Returns
    - string

### ConfigFromOpenshift().get_cfg_dct

[[find in source code]](../../viaa/openshift_helpers.py#L370)

```python
def get_cfg_dct():
```

- use this to get the conf in your app
- Returns
   - dict

### ConfigFromOpenshift().update_local_cfg

[[find in source code]](../../viaa/openshift_helpers.py#L383)

```python
def update_local_cfg():
```

- updates a local configfile from secret in openshift

### ConfigFromOpenshift().update_oc_cfg

[[find in source code]](../../viaa/openshift_helpers.py#L399)

```python
def update_oc_cfg():
```

- uploads content from local yamlfile to openshift secret

## CreatePipeline

[[find in source code]](../../viaa/openshift_helpers.py#L26)

```python
class CreatePipeline():
    def __init__(
        app,
        host,
        token,
        namespace='ci-cd',
        interactive=False,
        gitname=None,
    ):
```

Creates a pipeline in openshift

## CreateTemplate

[[find in source code]](../../viaa/openshift_helpers.py#L99)

```python
class CreateTemplate():
    def __init__(app, host, token, namespace='openshift', interactive=False):
```

Creates a openshift template with a deployentconfig and a service

Args

- app: app name
- host,
- token
