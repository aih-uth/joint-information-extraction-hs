import pandas as pd
import os


def get_entity(df):
    tokens, labels, indexs = list(df["word"]), list(df["IOB"]), list(df["index"])
    seqs, tags, ids = [], [], []
    for i in range(0, len(tokens), 1):
        if labels[i].startswith("B-"):
            if i == len(labels) - 1:
                seqs.append(tokens[i])
                tags.append(labels[i])
                ids.append([int(indexs[i])])
            else:
                tmp1, tmp2, tmp3 = [tokens[i]], [labels[i]], [int(indexs[i])]
                for j in range(i+1, len(tokens), 1):
                    if labels[j].startswith("I-"):
                        tmp1.append(tokens[j])
                        tmp2.append(labels[j])
                        tmp3.append(int(indexs[j]))
                        if j ==  len(labels) - 1:
                            seqs.append(" ".join(tmp1))
                            tags.append(" ".join(tmp2))
                            ids.append(tmp3)
                    else:
                        seqs.append(" ".join(tmp1))
                        tags.append(" ".join(tmp2))
                        ids.append(tmp3)
                        break  
    return tokens, labels, ids


def result2html_re(text, rel):
    text = """<tr class="tp">
                     <td></td>
                     <td><b>{0}</b></td>
                     <td>{1}</td>
                     </tr> """.format(rel, text)
    return text


def result2html_ner(text):
    text = """<tr class="tp">
                     <td></td>
                     <td>{0}</td>
                     </tr> """.format(text)
    return text


def insert_html_tag_re(words, ent, start, end, head_tail_falg):
    if abs(start - end) == 0:
        words[start] = "<span class=\"{2}\"><span class=\"type\">{0}</span>{1}</{0}></span>".format(ent, words[start], head_tail_falg)
    else:
        words[start] = "<span class=\"{2}\"><span class=\"type\">{0}</span>{1}".format(ent, words[start], head_tail_falg)
        # words[end] = "{0}</{1}></span>".format(words[end], ent)
        words[end] = "{0}</span>".format(words[end])
    return words


def insert_html_tag_ner(words, ent, start, end):
    if abs(start - end) == 0:
        words[start] = "<span class=\"{2}\"><span class=\"type\">{0}</span>{1}</{0}></span>".format(ent, words[start], "entity")
    else:
        words[start] = "<span class=\"{2}\"><span class=\"type\">{0}</span>{1}".format(ent, words[start], "entity")
        # words[end] = "{0}</{1}></span>".format(words[end], ent)
        words[end] = "{0}</span>".format(words[end])
    return words



def transform_result2html_ner(res_df):
    # テンプレートの読み込み
    with open("./lib/templates/entity_examples.html",'r') as file:
        ner_html = file.read()
    file.closed
    # ID
    _, _, ids = get_entity(res_df)
    words = list(res_df["word"])
    for t_ids in ids:
        head_start, head_end = t_ids[0], t_ids[-1] 
        # タグを挿入
        words = insert_html_tag_ner(words, res_df["IOB"][res_df["index"]==str(head_start)].iloc[0][2:], head_start, head_end)
    # formatの編集
    html_text = result2html_ner(" ".join(words))
    # 置換
    ner_html = ner_html.replace('{% ' + "text" + ' %}', " ".join(res_df["word"]))
    ner_html = ner_html.replace('{% ' + "results" + ' %}', html_text)
    return ner_html


def transform_result2html_re(res_df, spacy_format):
    # テンプレートの読み込み
    with open("./lib/templates/relation_examples.html",'r') as file:
        rel_html = file.read()
    file.closed
    # ID
    tokens, labels, ids = get_entity(res_df)
    html_list_re = []
    for rels in spacy_format["arcs"]:
        # 単語のリスト
        words = list(res_df["word"])
        # head/tailとなる固有表現
        head, tail = rels["start"], rels["end"]
        # index
        head_ids = [x for x in ids if int(head) in x][0]
        tail_ids = [x for x in ids if int(tail) in x][0]
        # 各固有表現の始点と終点　
        head_start, head_end = head_ids[0], head_ids[-1] 
        tail_start, tail_end = tail_ids[0], tail_ids[-1]
        # タグを挿入
        words = insert_html_tag_re(words, res_df["IOB"][res_df["index"]==str(head_start)].iloc[0][2:], 
                                                    head_start, head_end, "head")
        words = insert_html_tag_re(words, res_df["IOB"][res_df["index"]==str(tail_start)].iloc[0][2:], 
                                                    tail_start, tail_end, "tail")
        # htmlへ
        html_text = result2html_re(" ".join(words), rels["label"])
        html_list_re.append(html_text)
    # 置換
    rel_html = rel_html.replace('{% ' + "text" + ' %}', " ".join(res_df["word"]))
    rel_html = rel_html.replace('{% ' + "results" + ' %}', "\n".join(html_list_re))
    return rel_html