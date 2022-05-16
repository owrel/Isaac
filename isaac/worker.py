import dialoguemanager.intents as intents
from importlib import reload 
# Variables accessibility
# user_prompt
# previous_intent
# current_intent
# current_intents_list
# current_intent_name
# q
# self.intents

class Worker:
    def __init__(self):
        self.name = type(self).__name__


    def __call__(self):
        raise('Missing call function for worker ' + self.name)

    def get_parameters(self):
        return '()'


class CreatingIntents(Worker):
    def __init__(self):
        super().__init__()

    def get_parameters(self):
        return '(self.intents,self.model)'
    def __call__(self,intents_list,model):
        print('Sure, how would you like to name your new intent ?')
        name = input('#: ')
        examples = []
        done = False
        print('I will require examples to learn from them, type "DONE" once you are done.')
        while done == False:
            ex = input(f'# example {str(len(examples)+1)}: ')
            if ex == 'DONE':
                done = True
                continue
            else:
                examples.append(ex)
        intent = intents.Intent(name=name,examples=examples)
        intents_list.append(intent)
        model.encode_examples(intents_list)
        intents.Intent.save_intents(intents_list)


                    
# Added by Isaac on 11/19/2021, 02:04:08 on request
class ListIntent(Worker):
    def __init__(self):
        super().__init__()

    def get_parameters(self):
        return '(self.intents)'

    def __call__(self,intent_list):
        print('Sure, here they are :')
        for i,index in zip(intent_list,range(len(intent_list))):
            print(f'\t{str(index+1)}: {i.name}')

                    

                    
# Added by Isaac on 11/19/2021, 02:13:14 on request
class PreviousSimilarity(Worker):
    def __init__(self):
        super().__init__()

    def get_parameters(self):
        return '(previous_intents_list)'

    def __call__(self,previous_sim):
        if len(previous_sim) > 0:
            if len(previous_sim) >=5 : rge = 5 
            else : rge = len(previous_sim)
            for i in previous_sim[:5]:
                print(f'\t{i[0]} : {i[1]}')
        else:
            print('No previous request to show Sir.')

                    

                    
# Added by Isaac on 11/19/2021, 02:29:38 on request
class ReloadWorker(Worker):
    def __init__(self):
        super().__init__()

    def get_parameters(self):
        return '(worker)'

    def __call__(self,wkr):
        reload(wkr)
        print('Workers reloaded')

                    
# Added by Isaac on 11/19/2021, 02:33:25 on request
class ReloadIntents(Worker):
    def __init__(self):
        super().__init__()

    def get_parameters(self):
        return '(self.intents)'

    def __call__(self,li):
        intents.Intent.save_intents(li)

                    

                    
# Added by Isaac on 11/20/2021, 01:03:37 on request
class GetExamplesFromIntent(Worker):
    def __init__(self):
        super().__init__()

    def get_parameters(self):
        return '(self.intents,self)'

    def __call__(self,li,dm):
        print('Which intent would you like me to show their examples ?')
        q = False
        while q == False:
            ui = input('#: ')
            if dm.get_intent(ui)[0][0] == 'ListIntent':
                w = ListIntent()
                w(li)
            else :
                for i in li:
                    if i.name.upper() == ui.upper():
                        for e in i.examples:
                            print('\t '+e)
                        q = True
                        continue
                if q:
                    continue
                else:
                    print("I couldn't find the intent, you can ask me to show the intent if you want.")    
