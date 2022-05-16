from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import sys
import json as JSON
import time


def into_space(s):
    ret = ''
    for i in range(len(s)):
        ret += ' '
    return ret


class Model:
    existing_model = {
        'minilm': "all-MiniLM-L12-v1",
        'mpnet': 'all-mpnet-base-v2',
        'qa-mpnet-dot': "multi-qa-mpnet-base-dot-v1",
        'qa-mpnet-cos': "multi-qa-mpnet-base-cos-v1",
        'roberta': "all-distilroberta-v1",
        'msmacro': 'msmarco-distilbert-dot-v5',
        'tinybert': 'paraphrase-TinyBERT-L6-v2',
        'albert': 'paraphrase-albert-small-v2'
    }

    @staticmethod
    def compute_performance(intents):
        result_global = {}
        local_intents = intents.copy()
        for k in Model.existing_model:
            # print(k,value)
            result = {}
            print('Evaluating ' + k)
            name = Model.existing_model[k]
            result[k] = {"name": name}
            model = Model(k)
            model.encode(local_intents)

            all_time = []

            nb_fail = 0
            nb_success = 0

            for i in local_intents:
                result[i.name] = {'examples_results': []}
                for ex in i.examples:
                    example_result = {
                        "example": ex,
                    }
                    for res_type in ['mean', 'max', 'meanmax']:
                        start = time.time()
                        ret = model.compute_intent_similarity(
                            ex, local_intents, res_type=res_type)
                        ret = sorted(
                            ret.items(), key=lambda x: x[1], reverse=True)
                        total = time.time()-start
                        all_time.append(total)
                        example_result[res_type] = {
                            'time': total,
                            'awaited': i.name,
                            'obtained': ret[0][0],
                            'confidence': ret[0][1],
                            'success': (ret[0][0] == i.name)
                        }

                        if not res_type in  result[i.name]:
                            result[i.name][res_type] = 0
                        if ret[0][0] == i.name:
                            result[i.name][res_type] += 1
                            nb_success += 1
                        else:
                            nb_fail += 1

                    result[i.name]['examples_results'].append(
                        example_result
                    )

            result['sum_time'] = sum(all_time)
            result['mean_time'] = sum(all_time)/len(all_time)
            result['nb_fail'] = nb_fail
            result['nb_success'] = nb_success

            result_global[k] = {
                'sum_time': sum(all_time),
                'mean_time': sum(all_time)/len(all_time),
                'nb_succes' : nb_success,
                'nb_fail' : nb_fail, 
                }

            with open(f'model_evaluation/{name}_result.json', 'w') as outfile:
                JSON.dump(result, outfile, indent=2)

        with open(f'model_evaluation/global_result.json', 'w') as outfile:
            JSON.dump(result_global, outfile, indent=2)

    def __init__(self, name):
        self.name = name
        print('Initializing model based on ' + name)
        self.model = SentenceTransformer(self.existing_model[self.name])

    def encode(self, intents):
        ret = 0
        if type(intents) == type([]):
            update_progress(0)
            for i, n in zip(intents, range(len(intents))):
                update_progress(n/len(intents), status=i.name)
                if i.need_encoding or i.previous_encoder != self.existing_model[self.name]:
                    if len(i.examples) > 0:
                        i.encoded_examples = self.model.encode(i.examples)
                        ret += 1
                    i.previous_encoder = self.name
                    i.need_encoding = False
                update_progress(n/len(intents), status=into_space(i.name))
            update_progress(1)

        print('Intents encoding needed : ' + str(ret))

    def compute_intent_similarity(self, input, intents, res_type='mean'):
        result = {}
        for i in intents:
            if i.need_encoding:
                if len(i.examples) > 0:
                    encoded_examples = self.model.encode(i.examples)
                    i.encoded_examples = encoded_examples
                else:
                    print('No example avaiable for Intent ' + i.name + ', pass.')
                    return [0]
            else:
                if i.previous_encoder != self.name:
                    encoded_examples = self.model.encode(i.examples)
                    i.encoded_examples = encoded_examples
                else:
                    encoded_examples = i.encoded_examples

            encoded_input = self.model.encode(input)

            similarity = cosine_similarity(
                [encoded_input],
                encoded_examples
            )
            result[i.name] = similarity[0]

        if res_type == 'all':
            return result
        elif res_type == 'mean':
            for i in result:
                result[i] = float(sum(result[i])/len(result[i]))
            return result
        elif res_type == 'max':
            for i in result:
                result[i] = float(max(result[i]))
            return result
        elif res_type == 'meanmax':
            for i in result:
                result[i] = float(
                    (max(result[i]) + sum(result[i])/len(result[i])) / 2)
            return result
        else:
            return result


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
    text = "\rEncoding intents : [{0}] {1}% {2}".format(
        "#"*block + "-"*(barLength-block), progress*100//1, status)
    sys.stdout.write(text)
    sys.stdout.flush()
