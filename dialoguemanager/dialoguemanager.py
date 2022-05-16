import json
import os
import keyword
import sys
from importlib import reload
from datetime import datetime

from .cmdmanager import *
from .intents import *
from .models import *





class DialogueManager:
    def __init__(self, model):
        self.model = model
        print('Initializing Dialogue Manager on directory :', os.getcwd())
        self.init_intents()
        print('Initializing done.\n')
        self.cmdmanager = CmdManager()
        self.DM()
        Intent.save_intents(self.intents)

    def get_intent(self, user_input):
        result = self.model.compute_intent_similarity(
            user_input, self.intents, res_type='meanmmax')
        return sorted(result.items(), key=lambda x: x[1], reverse=True)


    
        

#     def DM(self):
#         self.greetings()
#         user_input = ''
#         history = []
#         previous_intent = None
#         previous_intents_list = []
#         current_intent = None
#         current_intents_list = []
#         current_intent_name = None
#         q = False
#         while q == False:

#             user_input = input('#: ')
#             history.append(user_input)

#             previous_intents_list = current_intents_list
#             current_intents_list = self.get_intent(user_input)
#             previous_intent = current_intent
#             current_intent = current_intents_list[0]
#             current_intent_name = current_intent[0]

#             if user_input == 'END' or current_intent_name == 'Quit' or current_intent_name == "Goodbye":
#                 q = True
#                 continue

#             wkr_str = 'worker.'+current_intent_name+'()'
#             try:
#                 wkr = eval(wkr_str)
#                 rep = eval('wkr' + wkr.get_parameters())
#             except AttributeError:
#                 print(
#                     f'It seems like no worker called "{current_intent_name}" exist. Should I add a skeleton function to the worker file ?')
#                 ui = input('#: ')
#                 if self.get_intent(ui)[0][0] == 'Confirm':
#                     now = datetime.now()
#                     date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
#                     f = open("worker/worker.py", "a")
#                     f.write(f"""

                    
# # Added by Isaac on {date_time} on request
# class {current_intent_name}(Worker):
#     def __init__(self):
#         super().__init__()

#     def get_parameters(self):
#         return '()'

#     def __call__(self):
#         print(self.name + ' has been called (Default message from generation)')

#                     """)
#                     f.close()
#                     print(f'Worker {current_intent_name} added.')
#                     reload(worker)
#             except KeyboardInterrupt:
#                 print('\nLeaving worker...')

#         print('See you next time sir.')

#     def greetings(self):
#         now = datetime.now()
#         hour = int(now.strftime("%H"))
#         if hour <= 5 or hour >= 18:
#             print(
#                 'Good evening sir, hope you\'re having a good night. How I may help you ?')
#         elif hour <= 11:
#             if hour <= 8:
#                 print(
#                     'Good morning sir. Nice to see you awake that early. How I may help you ?')
#             else:
#                 print('Good morning sir. Hope you doing well. How I may help you ?')
#         else:
#             print('Hello sir. Nice to see you there. How I may help you ?')

    def init_intents(self):
        print('Importing intents...')
        self.intents = Intent.load_intents(self.model.name)
        nb = self.model.encode_examples(self.intents)
        print('Encoded ' + str(nb) + ' intents(s)')
        print('Importing intents done.')


    def intent_decision(self, intent, intent_sim):
        pass

    def process_input(self, input):
        self.info['history'].append(input)
        self.info['previous_intents_list'] = self.info['current_intents_list']
        self.info['current_intents_list'] = self.get_intent(input)
        self.info['previous_intent'] = self.info['current_intent']
        self.info['current_intent'] = self.info['current_intents_list'][0]
        self.info['current_intent_name'] = self.info['current_intent'][0]
        self.cmdmanager.update_information(f"{self.info['current_intents_list'][0]},{self.info['current_intents_list'][1]}")


        


    def DM(self):
        self.info = {
            "user_input": '',
            "history": [],
            "previous_intent": None,
            "previous_intents_list": [],
            "current_intent": None,
            "current_intents_list": [],
            "current_intent_name": None,
            "quit": False,
            "statistics": {},
            "context": "Init",
            'cmd': {
                'groundcmd': self.cmdmanager,
                'constructor' : CmdManager
            }
        }

        self.cmdmanager.set_callfunction(self.process_input)
        self.cmdmanager.cmdloop()




        