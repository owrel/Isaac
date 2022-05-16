import os
import json
import numpy as np


class Intent:
    def __init__(self, json=None, name=None, current_encoder=None,examples=None):
        if name == None:
            raise NameError('Intents require at least a name')
        else :
            self.name = name

        if json != None:  
            if 'examples' in json:
                self.examples = json['examples']
            else :
                self.examples = []
            if 'encoded_examples' in json:
                self.encoded_examples = np.array(json['encoded_examples'])
            else :
                self.encoded_examples = []


            ## Need encoding check
            if not 'need_encoding' in json:
                self.need_encoding = False
            else :
                self.need_encoding = json['need_encoding']

            if len(self.encoded_examples) != len(self.examples):
                self.need_encoding = True
                

            if 'previous_encoder' in json:
                if json['previous_encoder'] != current_encoder:
                    self.need_encoding = True
                self.previous_encoder = json['previous_encoder']
            else :
                self.previous_encoder = None
                self.need_encoding = True

        else:
            self.examples = examples
            self.current_encoder = current_encoder
            self.need_encoding = True
            self.encoded_examples = []