from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import time, sys


def into_space(s):
    ret = ''
    for i in range(len(s)):
        ret += ' '
    return ret


class Model:
    def __init__(self, name):
        self.name = name
        print('Initializing model based on ' + name)

    def encode_examples(self,intents):
        ret = 0
        
        if type(intents) == type([]):
            update_progress(0)
            for i,n in zip(intents,range(len(intents))):
                update_progress(n/len(intents),status=i.name)
                if i.need_encoding:
                    if len(i.examples) > 0:
                        i.encoded_examples = self.model.encode(i.examples)
                        ret +=1
                    i.previous_encoder = self.name
                    i.need_encoding = False
                update_progress(n/len(intents),status=into_space(i.name))
            update_progress(1)


        return ret
    

    def compute_intent_similarity(self,input,intents,res_type='mean'):
        result = {}
        for i in intents:
            if i.need_encoding :
                if len(i.examples) > 0:
                    encoded_examples = self.model.encode(i.examples)    
                    i.encoded_examples = encoded_examples
                else:
                    print('No example avaiable for Intent ' + i.name +', pass.')
                    return [0]
            else:
                if i.previous_encoder != self.name:
                    encoded_examples = self.model.encode(i.exemples)
                    i.encoded_examples = encoded_examples
                else :
                    encoded_examples = i.encoded_examples
                

            encoded_input = self.model.encode(input)

            similarity = cosine_similarity(
                [encoded_input],
                encoded_examples
            )
            result[i.name] = similarity[0]


        if res_type == 'all' :
            return result
        elif res_type == 'mean' :
            for i in result:
                result[i] = sum(result[i])/len(result[i])
            return result
        elif res_type == 'max':
            for i in result:
                result[i] = max(result[i])
            return result
        elif res_type == 'meanmmax':
            for i in result:
                result[i] = (max(result[i]) + sum(result[i])/len(result[i])) / 2
            return result
        else :
            return result

        
        


        
    


class BertSim(Model):
    def __init__(self):
        super().__init__('BertSim')
        self.model_name = 'bert-base-nli-mean-tokens'
        self.model = SentenceTransformer(self.model_name)
        print('Done.')

    
class MiniLM(Model):
    def __init__(self):
        super().__init__('MiniLM')
        self.model_name = 'all-MiniLM-L6-v2'
        self.model = SentenceTransformer(self.model_name)
        print('Done.')



def update_progress(progress, status='', barLength=10):
    # barLength = 10 # Modify this to change the length of the progress bar
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rLoading intents : [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100//1, status)
    sys.stdout.write(text)
    sys.stdout.flush()