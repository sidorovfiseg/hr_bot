import pickle
import numpy as np
from markdown_it import MarkdownIt
import os
import ml
from ml.preprocess import *
from ml import model_embedding, tokenizer_answer, model_answer

from transformers import GenerationConfig

generation_config = GenerationConfig(
    temperature = 1,
    max_length = 120,
    num_beams = 6,
    repetition_penalty = 1.4,
    do_sample = False
)

def query_message(introduction: str, s: str):
    text = f"\n\nТекст: {s}"
    return introduction + text
def remove_chars_except(input_string):
    ban_list = ["*", "-", "(", ")", "\n", "'", "\"", "\\", "/"]
    for char in ban_list:
        input_string = input_string.replace(char, ' ')
    input_string = input_string.lower()
    return input_string
def get_chapters(filename):
    with open(filename, encoding='utf-8') as f:
        content = f.read()
    md = MarkdownIt()
    tokens = md.parse(content)
    res = []
    s = ''
    for i in range(len(tokens) - 3):
        if tokens[i].type == 'heading_open' and tokens[i + 3].type != 'heading_open':
            if s:
                res.append(s)
            s = ''
        elif tokens[i].type == 'inline':
            s += ' ' + remove_chars_except(tokens[i].content)
    res.append(s)
    return res
def process_chapters(filename):
    chapters = get_chapters(filename)
    chapters_array = np.empty(len(chapters), dtype=object)
    for i in range(len(chapters)):
        chapter_text = chapters[i][:2000]  # Обрезаем главу до 2000 буквенных символов
        chapters_array[i] = chapter_text  # Добавляем обрезанную главу в массив NumPy
    return chapters_array

def get_chapters_and_embeds(filename):
    inputs = process_chapters(filename)
    questions = np.empty(len(inputs), dtype=object)
    a = "Задача - сгенерировать семь независимых вопросов на которые отвечает следующий контекст."
    b = ""
    introduction = f"{a}\n{b}"

    for j, str in enumerate(inputs):
        final_text = query_message(introduction, str)
        data = tokenizer_answer(final_text, return_tensors="pt")
        data = {k: v.to(model_answer.device) for k, v in data.items()}
        output_ids = model_answer.generate(
            **data,
            generation_config=generation_config
        )[0]
        print("====================")
        ans = tokenizer_answer.decode(output_ids.tolist(), skip_special_tokens=True).split('\n')
        questions[j] = [re.sub(r'^\d+\.\s*', '', i) for i in   ans]

    res = []
    for chapter in questions:
        temp = []
        for question in chapter:
            temp.append(model_embedding.encode(prepare_text(question), convert_to_tensor=True))
        res.append(temp)
    return inputs, res

def embed_request(request):
    return model_embedding.encode(request, convert_to_tensor=True).to(model_embedding.device)
def save_data(filename):
    text, embeds = get_chapters_and_embeds(filename)
    with open('text.pkl', 'wb') as f:
        pickle.dump(text, f)
    with open('embeds.pkl', 'wb') as f:
        pickle.dump(embeds, f)
def add_file_to_data(filename):
    new_text, new_embeds = get_chapters_and_embeds(filename)
    if os.path.exists('text.pkl') and os.path.exists('embeds.pkl'):
        print('ДОБАВЛЯЮ')
        # Оба файла существуют
        with open('text.pkl', 'rb') as f:
            text = pickle.load(f)
        with open('embeds.pkl', 'rb') as f:
            embeds = pickle.load(f)
    else:

        print('СОЗДАЮ')
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

if __name__ == "__main__":
    add_file_to_data('../data/code.md')