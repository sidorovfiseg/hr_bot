import pickle

from markdown_it import MarkdownIt
import os

import ml
from ml.preprocess import *

from ml import model_embedding, update



def get_chapters(filename):
    with open(filename, encoding='utf-8') as f:
        content = f.read()
    md = MarkdownIt()
    tokens = md.parse(content)
    res = []
    s = []
    for i in range(len(tokens)):
        if tokens[i].type == 'heading_open':
            if s:
                res.append(s)
            s = []
        elif tokens[i].type == 'inline':
            s += split_sentences(tokens[i].content)
    if(s):
        res.append(s)
    return res

def get_chapters_and_embeds(filename):
    res = []
    chapters = get_chapters(filename)
    print(chapters[0])
    for chapter in chapters:
        temp = []
        for sentence in chapter:
            temp.append(model_embedding.encode( prepare_text(sentence), convert_to_tensor=True))
        res.append(temp)
    return chapters, res

def embed_request(request):
    return model_embedding.encode(request, convert_to_tensor=True)

def save_data(filename):
    text, embeds = get_chapters_and_embeds(filename)
    with open('text.pkl', 'wb') as f:
        pickle.dump(text, f)
    with open('embeds.pkl', 'wb') as f:
        pickle.dump(embeds, f)

def add_file_to_data(filename):
    new_text, new_embeds = get_chapters_and_embeds(filename)
    if os.path.exists('text.pkl') and os.path.exists('embeds.pkl'):
        # Оба файла существуют
        with open('text.pkl', 'rb') as f:
            text = pickle.load(f)
        with open('embeds.pkl', 'rb') as f:
            embeds = pickle.load(f)
    else:
        # Один или оба файла отсутствуют, создаем новые списки
        text = []
        embeds = []
    text.extend(new_text)
    embeds.extend(new_embeds)

    ml.text_data = text
    ml.embeds_data = embeds

    with open('text.pkl', 'wb') as f:
        pickle.dump(text, f)
    with open('embeds.pkl', 'wb') as f:
        pickle.dump(embeds, f)



