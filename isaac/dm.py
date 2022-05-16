from typing import Any
from .cmdmanager import *
from .model import *

import os



class Context:
    def __init__(self, intent_list=[], input_str=None):
        self.intent_list = intent_list
        self.input_str = input_str



class WrongIntent(Exception):
    pass


class DialogueManager:
    def __init__(self, model: Model, intents, name,
                 prefix="#- : ", information=os.getcwd(), 
                 ):
        self.model = model
        self.intents = intents
        self.name = name
        self.console_manager = CmdManager(
            prefix=prefix)

        self.history = []
        self.context = Context()
        self.console_manager.callback = self.process_input

        
        try :
            self.console_manager.cmdloop("Hello world")
        except(KeyboardInterrupt):
            print('Leaving current context...')


    def compute_input_sim(self, input_str,context):
        raw_output = self.model.compute_intent_similarity(input_str, self.intents)
        ret = sorted(raw_output.items(), key=lambda x: x[1], reverse=True)
        return ret


    def verify_intent(self, intent_list):
        pass

        
    def process_input(self,line):
        intent_list = self.compute_input_sim(line,self.context)
        self.history.append(self.context)
        self.context = Context(intent_list=intent_list,input_str=line)
        self.verify_intent(intent_list) # do stuff
        

        


    def on_wrong_intent(self):
        print('Wrong intent')

    def on_quit(self):
        pass
            

