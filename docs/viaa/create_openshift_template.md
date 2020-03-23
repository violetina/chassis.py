# Create Openshift Template

> Auto-generated documentation for [viaa.create_openshift_template](../../viaa/create_openshift_template.py) module.

Created on Wed Feb  5 15:37:04 2020

- [Chassis](../README.md#viaa-chassis) / [Modules](../MODULES.md#chassis-modules) / [Viaa](index.md#viaa) / Create Openshift Template

- Description

- Function __main__ used in console script openshift-create-template.
- Will use opneshift api no oc needed!
- Creates a template with a deploymentconfig and service
- (use add to project from catalog, if no namespace is given. Else, in the given namespace add from project)

- Usage

- bash # openshift-create-template --app <appname> --host <openshift api endpoint> --token <oc whoami -t --namespace <openshift project name> --interactive <ask for all args>

@author: tina
