import pickle
import re

from markdown_it import MarkdownIt
import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, GenerationConfig
import numpy as np

model_name = "IlyaGusev/fred_t5_ru_turbo_alpaca"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to("cuda")

model.eval()

def remove_chars_except(input_string):
    ban_list = ["*", "-", "(", ")", "\n", "'", "\""]
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

file = "data/code.md"
chapters = get_chapters(file)

def process_chapters(filename):
    chapters = get_chapters(filename)
    chapters_array = np.empty(len(chapters), dtype=object)
    for i in range(len(chapters)):
        chapter_text = chapters[i][:2000]  # Обрезаем главу до 2000 буквенных символов
        chapters_array[i] = chapter_text  # Добавляем обрезанную главу в массив NumPy

    return chapters_array

def query_message(introduction: str, s: str):
    text = f"\n\nТекст: {s}"
    return introduction + text

generation_config = GenerationConfig(
    temperature = 1,
    max_length = 120,
    num_beams = 6,
    repetition_penalty = 1.4,
    do_sample = False
)


print(get_chapters(file)[0])
print("==========================================================================================")

print(type(process_chapters(file)))

inputs = process_chapters(file)

a = "Задача - сгенерировать пять независимых вопросов на которые отвечает следующий контекст."
b = ""
introduction = f"{a}\n{b}"


for str in inputs:
    final_text = query_message(introduction, str)
    data = tokenizer(final_text, return_tensors="pt")
    data = {k: v.to(model.device) for k, v in data.items()}
    output_ids = model.generate(
        **data,
        generation_config=generation_config
    )[0]

    print("====================")
    print(tokenizer.decode(output_ids.tolist(), skip_special_tokens=True))