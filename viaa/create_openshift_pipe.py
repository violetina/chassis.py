#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 15:37:04 2020

@author: tina
"""


from viaa.openshift_helpers import CreatePipeline
import argparse



    
def __main__():
    '''Args:

        - path

          - path to watch'''
    arg_parse = argparse.ArgumentParser(description='Watcher dir')
    # Add the arguments
    arg_parse.add_argument('--app',
                           metavar='app',
                           type=str,
                           help='the name of the appp')
    arg_parse.add_argument('--host',
                          metavar='hostname',
                          type=str,
                          help='api url of openshift server')
    arg_parse.add_argument('--token',
                          metavar='token',
                          type=str,
                          help='oc whoami -t token')    
    arg_parse.add_argument('--gitname',
                          metavar='gitname',
                          type=str,
                          help='oc whoami -t token')  
    # Execute the parse_args() method
    args = arg_parse.parse_args()
    app = args.app
    host = args.host
    token= args.token
    gitname = args.gitname
    
    CreatePipeline(app=app,host=host,token=token,gitname=gitname)()

if __name__ == '__main__':
    # Create the parser
    __main__()