import torch
import torch.nn as nn
import torch.utils.data
from lib.models import CRF
from transformers import BertModel


class BERT_JOINT(nn.Module):
    def __init__(self, tag2idx, rel2idx, bert_path):
        super(BERT_JOINT, self).__init__()
        self.bert_model = BertModel.from_pretrained(bert_path)
        self.dropout = nn.Dropout(0.1)
        self.linear = nn.Linear(768, len(tag2idx))
        self.crf = CRF(tag2idx, batch_first=True)
        self.label_embedding = nn.Embedding(len(tag2idx), 30, padding_idx=0)
        self.U_prd = nn.Linear(768+30, 768+30)
        self.W_prd = nn.Linear(768+30, 768+30)
        self.V_pred = nn.Linear(768+30, len(rel2idx), bias=False)
    def forward(self, sentence, rel2idx):
        input_mask = (sentence != 0)
        embed = self.bert_model(sentence, attention_mask=input_mask, token_type_ids=None)
        embed = embed["last_hidden_state"][:, 1: -1,:]
        embed = self.dropout(embed)
        ner_output = self.linear(embed)
        le = self.label_embedding(torch.tensor(self.crf.decode(ner_output)))
        hx = torch.cat([embed, le], axis=2)
        seq_len = len(sentence[0]) - 2
        res = []
        for i in range(0, seq_len, 1):
            target = hx[:, i, :].expand(seq_len, (embed.shape[0]), -1).transpose(0, 1)
            p_head = self.V_pred(torch.tanh(self.U_prd(target) + self.W_prd(hx)))
            p_head[:, i, rel2idx["None"]] = 100
            res.append(p_head)
        return self.crf.decode(ner_output), res