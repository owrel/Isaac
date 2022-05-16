from .model import *
from .intent import *
from .dm import *
######################
import json
import os


class Isaac:
    def __init__(
        self,
        model_name,
        path_data="data/"
    ):

        self.model = Model(model_name)
        self.path_data = path_data
        self.intents = self.load_intents()
        Model.compute_performance(self.intents)
        self.model.encode(self.intents)
        self.dm = DialogueManager(
            model=self.model, intents=self.intents, name='base')

        self.save_intents()

    def load_intents(self):
        """
            Load intents from path
        """
        print('Loading intents...')
        if os.path.isdir(self.path_data):
            if os.path.isfile(f'{self.path_data}intents.json'):
                with open(f'{self.path_data}intents.json') as json_file:
                    try:
                        data = json.load(json_file)
                        if os.path.isfile(f'{self.path_data}intents_encodings.json'):
                            with open(f'{self.path_data}intents_encodings.json') as json_file:
                                try:
                                    encoded_ex = json.load(json_file)

                                except Exception as e:
                                    print(
                                        'Error while loading encoded examples from intents')
                                    print(e)
                                    f = open(
                                        f'{self.path_data}_encodings.json', "w")
                                    f.write("{}")

                        else:
                            f = open(
                                f'{self.path_data}intents_encodings.json', "w")
                            f.write("{}")
                            encoded_ex = []

                        for e in encoded_ex:
                            if e in data:
                                data[e]['encoded_examples'] = encoded_ex[e]

                        intents = []
                        for i in data:
                            intents.append(
                                Intent(json=data[i], name=i, current_encoder=self.model.name))

                        return intents

                    except Exception as e:
                        print(
                            'Intents database is corrupted or not json-convertible.')
                        print('Error :', e)

                        answer = input(
                            'Should I recreate the intent database ? y/[n]')
                        if answer.upper() == 'Y':
                            f = open(f'{self.path_data}intents.json', "w")
                            f.write("{}")

            else:
                print('No intents databse found, creating file.')
                f = open(f'{self.path_data}intents.json', "w")
                f.write("{}")

        else:
            print(
                'No repertories loading/saving directory found. Creating tree structure.')
            os.mkdir(self.path_data)
            f = open(f'{self.path_data}intents.json', "w")
            f.write("{}")
            f.close()

    def save_intents(self) -> None:
        """
        Save intents into encodings and raw values
        """
        j_file = {}
        j_file_encoded = {}
        for i in self.intents:
            j_file[i.name] = {}
            j_file[i.name]['examples'] = i.examples
            j_file_encoded[i.name] = i.encoded_examples.tolist()
            j_file[i.name]['previous_encoder'] = i.previous_encoder
            j_file[i.name]['examples'] = i.examples

        # No folder checking required
        file_data = json.dumps(j_file, indent=2)
        f = open(f"{self.path_data}intents.json", "w")
        f.write(file_data)
        file_data = json.dumps(j_file_encoded)
        f = open(f"{self.path_data}intents_encodings.json", "w")
        f.write(file_data)
