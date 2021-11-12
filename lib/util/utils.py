import pandas as pd
import numpy as np
import torch
import torch.utils.data
from lib.models import BERT_JOINT
import json


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


def load_model(paras):
    tag2idx = json.load(open(paras.tag2idx_path, 'r'))
    rel2idx = json.load(open(paras.rel2idx_path, 'r'))
    model = BERT_JOINT(tag2idx, rel2idx, paras.bert_path)
    model.load_state_dict(torch.load('{0}'.format(paras.model_path),  map_location='cpu'))
    return model, tag2idx, rel2idx


def decode_ner(ner_preds, tag2idx):
    idx2tag = {int(v): k for k,v in tag2idx.items()}
    return [idx2tag[p] for pred in ner_preds for p in pred]


def decode_re(tokens, re_preds, ner_preds, rel2idx):
    idx2rel = {v: k for k, v in rel2idx.items()}
    decode_re = []
    for pred in re_preds:
        decode_re.append([idx2rel[x] for x in torch.argmax(pred, dim=2).detach().view(-1).cpu().numpy()])
    # Spacy
    ex = {"words": [], "arcs": []}
    for i in range(0, len(tokens), 1):
        res = decode_re[i]
        ex["words"].append({"text": tokens[i], "tag": ner_preds[i]})
        if len(set(res)) == 1 and res[0] == "None":
            pass
        else:
            for j in range(0, len(res), 1):
                if res[j] != "None":
                    if i > j:
                        ex["arcs"].append({"start": i, "end": j, "label": res[j], "dir": "right"})
                    else:
                        ex["arcs"].append({"start": i, "end": j, "label": res[j], "dir": "left"})
                else:
                    pass
    return ex


def spacy2df(spacy_format, name):
    for dct in spacy_format["words"]:
        dct["index"] = "None"
        dct["rel_type"] = []
        dct["tail_index"] = []
    for dct in spacy_format["arcs"]:
        head, tail, label = dct["start"], dct["end"], dct["label"]
        spacy_format["words"][head]["rel_type"].append(label)
        spacy_format["words"][head]["tail_index"].append(str(tail))
    index_cnt = 0
    for dct in spacy_format["words"]:
        dct["index"] = str(index_cnt)
        index_cnt += 1
        if len(dct["rel_type"]) == 0:
            dct["rel_type"].append("None")
            dct["tail_index"].append("None")
    dct4csv = {"index": [], "word": [], "IOB": [], "rel_type": [], "tail_index": []}
    for dct in spacy_format["words"]:
        dct4csv["index"].append(dct["index"])
        dct4csv["word"].append(dct["text"])
        dct4csv["IOB"].append(dct["tag"])
        dct4csv["rel_type"].append(",".join(dct["rel_type"]))
        dct4csv["tail_index"].append(",".join(dct["tail_index"]))
    pd.DataFrame(dct4csv.values(), index=dct4csv.keys()).T.to_csv("./results/" + name, index=False)
    return pd.DataFrame(dct4csv.values(), index=dct4csv.keys()).T