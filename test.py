import pickle
from markdown_it import MarkdownIt
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, GenerationConfig
import numpy as np

model_name = "IlyaGusev/fred_t5_ru_turbo_alpaca"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to("cuda")

model.eval()







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