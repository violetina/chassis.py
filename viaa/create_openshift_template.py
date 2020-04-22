#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 15:37:04 2020

- Description

        - Function __main__ used in console script openshift-create-template. 
        - Will use opneshift api no oc needed! 
        - Creates a template with a deploymentconfig and service 
        - (use add to project from catalog, if no namespace is given. Else, in the given namespace add from project)
    
- Usage

        - bash # openshift-create-template --app <appname> --host <openshift api endpoint> --token <oc whoami -t --namespace <openshift project name> --interactive <ask for all args> 

@author: tina
"""


from viaa.openshift_helpers import CreateTemplate
import argparse



    
def __main__():
    ''' add args with argparse  '''
    arg_parse = argparse.ArgumentParser(description='Creates a openshift template')
    # Add the arguments
    arg_parse.add_argument('--app',
                           metavar='app',
                           type=str,
                           help='the name of the appp')
    arg_parse.add_argument('--host',
                          metavar='hostname',
                          type=str,
                          default=None,

                          help='api url of openshift server')
    arg_parse.add_argument('--token',
                          metavar='token',
                          type=str,
                          default=None,
                          help='oc whoami -t token')    
                      
    arg_parse.add_argument('--namespace',
                          metavar='namespace',
                          type=str,
                          default='openshift',
                          help='asks for args')  
    arg_parse.add_argument('--interactive',
                          metavar='interactive',
                          type=str,
                          default=False,
                          help='asks for args')
    arg_parse.add_argument('--tofile',
                          metavar='tofile',
                          type=bool,
                          default=False,
                          help='create a yaml file in home dir')  
    # Execute the parse_args() method
    args = arg_parse.parse_args()
    app = args.app
    host = args.host
    token= args.token
    interactive = args.interactive
    namespace=args.namespace
    to_file=args.tofile
    
    CreateTemplate(app=app,
                   host=host,
                   token=token,
                   interactive=interactive,
                   to_file=to_file,
                   namespace=namespace)()

if __name__ == '__main__':
    # Create the parser
    __main__()