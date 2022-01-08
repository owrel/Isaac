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



    @staticmethod
    def load_intents(encoder):
        if os.path.isdir('data'):
            if os.path.isfile('data/intents.json'):
                with open('data/intents.json') as json_file:
                    try:
                        data = json.load(json_file)
                        
                        if os.path.isfile('data/intents_encodings.json'):
                            with open('data/intents_encodings.json') as json_file:
                                try:
                                    encoded_ex = json.load(json_file)
                                
                                except Exception as e:
                                    print('Error while loading encoded examples from intents')
                                    print(e)
                                    f = open("data/intents_encodings.json", "w")
                                    f.write("{}")
                            
                        else :
                            f = open("data/intents_encodings.json", "w")
                            f.write("{}")
                            encoded_ex = []

                        for e in encoded_ex:
                            if e in data:
                                data[e]['encoded_examples'] = encoded_ex[e]

                        intents = []
                        for i in data:
                            intents.append(Intent(json=data[i],name=i,current_encoder=encoder))

                        return intents

                    except Exception as e:
                        print(
                            'Intents database is corrupted or not json-convertible.')
                        print('Error :',e)
                        
                        answer = input('Should I recreate the intent database ? y/[n]')
                        if answer.upper() == 'Y':
                            f = open("data/intents.json", "w")
                            f.write("{}")
                            
            else:
                print('No intents databse found, creating file.')
                f = open("data/intents.json", "w")
                f.write("{}")

        else:
            print('No repertories \'data\' found. Creating tree structure.')
            os.mkdir('data')
            f = open("data/intents.json", "w")
            f.write("{}")
            f.close()


    @staticmethod
    def save_intents(intents):
        j_file = {}
        j_file_encoded = {}
        for i in intents :
            j_file[i.name] = {}
            j_file[i.name]['examples'] = i.examples
            j_file_encoded[i.name] = i.encoded_examples.tolist()
            j_file[i.name]['previous_encoder'] = i.previous_encoder 
            j_file[i.name]['examples'] = i.examples 

        # No folder checking required
        file_data = json.dumps(j_file,indent=2)
        f = open("data/intents.json", "w")
        f.write(file_data)
        file_data = json.dumps(j_file_encoded)
        f = open("data/intents_encodings.json", "w")
        f.write(file_data)
