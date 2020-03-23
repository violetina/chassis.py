#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 11:24:17 2020

@author: tina



"""
import os
import base64
from kubernetes import client
from openshift.dynamic import DynamicClient
import urllib3
import yaml
from pathlib import Path
home = str(Path.home())
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app='s3io'
aToken = "eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6Im1haW50ZW5hbmNlLXRva2VuLW1kbmNwIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6Im1haW50ZW5hbmNlIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiMzQ2NmI5OTktNDY5NS0xMWVhLWIzYzUtMDA1MDU2YTBhMzJjIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50OmRlZmF1bHQ6bWFpbnRlbmFuY2UifQ.fxhyny2rSgbUmTpjrHqI4W9mvCXmmg0SXX1DyJPeAqnmjO9TzdVZ1XPIHZPKzkklYrfSAaxztOB2AAavZakAY4Ra_HTMaI2HEtrgL0w-jmYLH8RGTf5Xr83Kgg-OhxSDumpAM7dLDK3n7qlKbHjTTj-yl5hDsTqKn-Sw14H2Dj5A9FMhqyvWJs9Ptxs7yl_5_bz131g3MMLqK5icuXZk3NNKJ1tIOB5WT6agwEOx08v6v2WqXVPnkYkd4m2_a0FAv7wSJ_eUX11NIyvLFAwUaY7HiCjId0myH7wyEuLNQjH60m6yjmGWazg9qL3jMwg6rS96WmTUfG0YmoTk5ZyaRw"
host="https://do-prd-okp-m0.do.viaa.be:8443"
namespace='viaa-tools'
gitname="hello-viaa-python"


class CreatePipeline():
    """Creates a pipeline in openshift"""
    def __init__(self,app,host,token,
                 namespace='ci-cd',
                 interactive=False,
                 gitname=None):
        self.gitname=gitname
        self.app=app
        self.token=token
        self.interactive=interactive
        self.host=host
        self.openshift_conf= client.Configuration()
        self.openshift_conf.host = host
        self.openshift_conf.verify_ssl = False
        self.openshift_conf.api_key = {"authorization": "Bearer " + self.token}
        self.openshift_apiclient = client.ApiClient(self.openshift_conf)
        self.dyn_client = DynamicClient(self.openshift_apiclient)
        self.v1_pipe = self.dyn_client.resources.get(api_version='build.openshift.io/v1',
                                                       kind='BuildConfig')
        self.pipeline={
            "apiVersion": "build.openshift.io/v1",
            "kind": "BuildConfig",
            "metadata": {
                "annotations": {
                    "from_chassis": "True"
                },
                "labels": {
                    "app": self.app,
                    "name": self.app+"-pipeline"
                },
                "name": self.app+"-pipeline",
                "namespace": "ci-cd",
            },
            "spec": {
                "failedBuildsHistoryLimit": 5,
                "nodeSelector": {},
                "output": {},
                "postCommit": {},
                "resources": {},
                "runPolicy": "Serial",
                "source": {
                    "git": {
                        "ref": "master",
                        "uri": "https://github.com/viaacode/" + self.gitname + ".git"
                    },
                    "sourceSecret": {
                        "name": "github"
                    },
                    "type": "Git"
                },
                "strategy": {
                    "jenkinsPipelineStrategy": {
                        "jenkinsfilePath": "OpenShift/Jenkinsfile"
                    },
                    "type": "JenkinsPipeline"
                },
                "successfulBuildsHistoryLimit": 10,
                "triggers": []
            },
            "status": {
                "lastVersion": 0
            }
        }
        if self.interactive:
            self.token = input('token:') 
            self.host= input('host:')
            self.app= input('app name(label in oc): ') 
    def __call__(self):
        self.v1_pipe.create(body=self.pipeline,
                               namespace='ci-cd')

#CreatePipeline(host=host,app=app,token=aToken,gitname=gitname)()   

class CreateTemplate():
    """
    Creates a openshift template with a deployentconfig and a service
    add template 
         Args
         
          - app: app name
          - host : api endpoint https://host:8443
          - token: oc whoami -t
          - namespace: the oc project
          - to_file :Bool default False
         
    creates a yaml file in user home if to_file=True
    """
    def __init__(self,app,host,token=None,
                 namespace='openshift',
                 interactive=False,
                 to_file=False
                 ):
        self.namespace=namespace
        self.app=app

        self.interactive=interactive
        self.host=host
        self.openshift_conf= client.Configuration()
        self.openshift_conf.host = host
        self.openshift_conf.verify_ssl = False
        if token:
            self.openshift_conf.api_key = {"authorization": "Bearer " + self.token}
            self.openshift_apiclient = client.ApiClient(self.openshift_conf)
            self.dyn_client = DynamicClient(self.openshift_apiclient)
            self.v1_template = self.dyn_client.resources.get(api_version='template.openshift.io/v1',
                                                           kind='Template')
        elif os.path.isfile(os.getcwd() + "/.openshift_token"):
            with open(os.getcwd() + "/.openshift_token", 'r') as fh:
                self.token=str(fh.readline()).rstrip()
                fh.close
            self.openshift_conf.api_key = {"authorization": "Bearer " + self.token}
            self.openshift_apiclient = client.ApiClient(self.openshift_conf)
            self.dyn_client = DynamicClient(self.openshift_apiclient)
            self.v1_template = self.dyn_client.resources.get(api_version='template.openshift.io/v1',
                                                           kind='Template')            
        else:
            print('no token found in .openshift_token or no token given as arg')
            raise FileNotFoundError    
        self.to_file = to_file
        self.template={
            "apiVersion": "template.openshift.io/v1",
            "kind": "Template",
            "metadata": {
                "creationTimestamp": "2020-01-07T15:18:40Z",
                "name": self.app,
        
            },
            "objects": [
                {
                    "apiVersion": "v1",
                    "kind": "Service",
                    "metadata": {
                        "annotations": {
                            "git-branch": "master",
                        },
                        "creationTimestamp": None,
                        "labels": {
                            "ENV": "${ENV}",
                            "app": self.app,
                            "component": "frontend"
                        },
                        "name": self.app+"-${ENV}"
                    },
                    "spec": {
                        "ports": [
                            {
                                "name": "http",
                                "port": 8080,
                                "protocol": "TCP",
                                "targetPort": 8080
                            }
                        ],
                        "selector": {
                            "ENV": "${ENV}",
                            "app": "app",
                            "type": "flask"
                        },
                        "sessionAffinity": "None",
                        "type": "ClusterIP"
                    },
                    "status": {
                        "loadBalancer": {}
                    }
                },
                {
                    "apiVersion": "apps.openshift.io/v1",
                    "kind": "DeploymentConfig",
                    "metadata": {
                        "annotations": {
                            "git-branch": "master"
                        },
                        "creationTimestamp": None,
                        "generation": 1,
                        "labels": {
                            "ENV": "${ENV}",
                            "app": self.app,
                            "type": "flask"
                        },
                        "name": self.app+"-${ENV}"
                    },
                    "spec": {
                        "replicas": 1,
                        "revisionHistoryLimit": 2,
                        "selector": {
                            "ENV": "${ENV}",
                            "app": self.app,
                            "type": "flask"
                        },
                        "strategy": {
                            "activeDeadlineSeconds": 21600,
                            "resources": {},
                            "rollingParams": {
                                "intervalSeconds": 1,
                                "maxSurge": "25%",
                                "maxUnavailable": "25%",
                                "timeoutSeconds": 600,
                                "updatePeriodSeconds": 1
                            },
                            "type": "Rolling"
                        },
                        "template": {
                            "metadata": {
                                "annotations": {
                                    "git-branch": "master"
                                },
                                "creationTimestamp": None,
                                "labels": {
                                    "ENV": "${ENV}",
                                    "app": self.app,
                                    "type": "flask"
                                }
                            },
                            "spec": {
                                "containers": [
                                    {
                                        "env": [
                                            {
                                                "name": "some_var",
                                                "value": "some_key"
                                            }
                                        ],
                                        "envFrom": [
                                            {
                                                "configMapRef": {
                                                    "name": self.app+"-${ENV}"
                                                }
                                            }
                                        ],
                                        "image": "docker-registry.default.svc:5000/" + self.namespace +'/' +self.app,
                                        "imagePullPolicy": "IfNotPresent",
                                        "name": self.app,
                                        "ports": [
                                            {
                                                "containerPort": 8080,
                                                "protocol": "TCP"
                                            }
                                        ],
                                        "resources": {
                                            "limits": {
                                                "cpu": "300m",
                                                "memory": "328Mi"
                                            },
                                            "requests": {
                                                "cpu": "100m",
                                                "memory": "128Mi"
                                            }
                                        },
                                        "terminationMessagePath": "/dev/termination-log",
                                        "terminationMessagePolicy": "File"
                                    }
                                ],
                                "dnsPolicy": "ClusterFirst",
                                "restartPolicy": "Always",
                                "schedulerName": "default-scheduler",
                                "securityContext": {
                                    "runAsUser": 101
                                },
                                "terminationGracePeriodSeconds": 10
                            }
                        },
                        "test": False,
                        "triggers": [
                            {
                                "imageChangeParams": {
                                    "automatic": True,
                                    "containerNames": [
                                        self.app
                                    ],
                                    "from": {
                                        "kind": "ImageStreamTag",
                                        "name": self.app+":${ENV}",
                                        "namespace": self.namespace
                                    },
                                    "lastTriggeredImage": ""
                                },
                                "type": "ImageChange"
                            },
                            {
                                "type": "ConfigChange"
                            }
                        ]
                    },
                    "status": {
        
                    }
                }
            ],
            "parameters": [
                {
                    "name": "ENV",
                    "value": "qas"
                }
            ]
        }
        if self.interactive:
            self.token = input('token:') 
            self.host= input('host:')
            self.app= input('app name(label in oc): ') 
            
    def __call__(self):
        if self.to_file:
            with open(os.path.join(home,self.app + '-tmpl.yaml'),'w') as fh:
                fh.writelines(yaml.dump(self.template))
                fh.close
            print(yaml.dump(self.template))
        else:
            self.v1_template.create(body=self.template,
                                    namespace=self.namespace) 

class ConfigFromOpenshift():
    """
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
    """
    def __init__(self,app,host,token=None, interactive=False,config_file=None,
                 yamlfile=None):
        self.app=app
        self.yamlfile=yamlfile
        if os.path.isfile(os.getcwd() + "/.openshift_token"):
  
            with open(os.getcwd() + "/.openshift_token", 'r') as fh:
                self.token=str(fh.readline()).rstrip()
                fh.close
        else:
            self.token=token
        self.config_file=config_file
        self.interactive=interactive
        self.host=host
        self.openshift_conf= client.Configuration()
        self.openshift_conf.host = host
        self.openshift_conf.verify_ssl = False
        self.openshift_conf.api_key = {"authorization": "Bearer " + self.token}
        self.openshift_apiclient = client.ApiClient(self.openshift_conf)
        self.dyn_client = DynamicClient(self.openshift_apiclient)
        self.v1_secret = self.dyn_client.resources.get(api_version='v1',
                                                       kind='Secret')

        
        if self.interactive:
            self.token = input('token:') 
            self.host= input('host:')
            self.app= input('app name(label in oc): ') 
        
    def get_cfg(self):
        """
           - Get the config from secret, yaml as string
           - Returns
               - string
        """
        s=self.v1_secret.get(label_selector='app=pygetsecret')
        app=s['items'][0]['data'][self.app]
        y=base64.b64decode(app).decode('utf-8')
        return str(y)
    
    def get_cfg_dct(self):
        """
           - use this to get the conf in your app
           - Returns
              - dict
        """
        
        s=self.v1_secret.get(label_selector='app=pygetsecret')
        app=s['items'][0]['data'][self.app]
        y=base64.b64decode(app).decode('utf-8')
        dct = yaml.safe_load(y)
        return dct
       
    def update_local_cfg(self):
        """
            - updates a local configfile from secret in openshift
        """
        try:
            y=self.get_cfg()
            if self.config_file:
                with open(self.config_file, 'w') as fh:
                    fh.writelines(y)
                    fh.close()
                return str(self.config_file)
            else:
                raise IOError         
        except Exception:
            raise

    def update_oc_cfg(self):
        """
            - uploads content from local yamlfile to openshift secret
        """
        with open (self.yamlfile, "rb") as fh:
            data=fh.read()
            encoded = base64.b64encode(data).decode("utf-8") 
        body = {
            'kind': 'Secret',
            'apiVersion': 'v1',
            'data': {self.app: encoded},
            'metadata': {'name': 'viaa-topsecret'},
            'spec': {
                'selector': {'app': self.app},
            }
        }
        try:
            self.v1_secret.patch(body=body, namespace='viaa-tools')
            return True
        except Exception as e:
            print(str(e))
            return False



