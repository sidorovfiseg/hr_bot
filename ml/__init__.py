import os
import pickle

from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import GenerationConfig

model_embedding = SentenceTransformer('all-MiniLM-L6-v2').to('cuda')

model_answer_name = "IlyaGusev/fred_t5_ru_turbo_alpaca"
generation_config_answer = GenerationConfig.from_pretrained(model_answer_name)
tokenizer_answer = AutoTokenizer.from_pretrained(model_answer_name)
model_answer= AutoModelForSeq2SeqLM.from_pretrained(model_answer_name).to("cuda")


print('Загрузка данных')

text_data = []
embeds_data = []

if os.path.exists('text.pkl') and os.path.exists('embeds.pkl'):
    with open('text.pkl', 'rb') as f:
        text_data = pickle.load(f)
    with open('embeds.pkl', 'rb') as f:
        embeds_data = pickle.load(f)

def update(t , e):
    global text_data
    global embeds_data
    text_data = t
    embeds_data = e