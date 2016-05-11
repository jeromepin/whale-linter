#!/usr/bin/env python3
import os
import json


class App:
    # @staticmethod
    # def remove(lst, element):
    #     ret = False
    #     if element in lst:
    #         lst.remove(element)
    #         ret = True
    #
    #     return ret

    @staticmethod
    def load_configuration():
        config_file = os.path.dirname(os.path.realpath(__file__)) + '/config.json'
        with open(config_file) as data_file:
            data = json.load(data_file)

        return data

    _config     = load_configuration.__func__()
    _collecter  = None
