import torch
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig, AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

MODEL_NAME = "IlyaGusev/saiga2_70b_lora"
DEFAULT_MESSAGE_TEMPLATE = "<s>{role}\n{content}</s>\n"
DEFAULT_SYSTEM_PROMPT = "Ты — Сайга, русскоязычный автоматический ассистент. Ты разговариваешь с людьми и помогаешь им."

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
version = torch.__version__
print(version)
print(device)


'''
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
generation_config = GenerationConfig.from_pretrained(MODEL_NAME)
print(generation_config)

inputs = ["Почему трава зеленая?", "Сочини длинный рассказ, обязательно упоминая следующие объекты. Дано: Таня, мяч"]
for inp in inputs:
    conversation = Conversation()
    conversation.add_user_message(inp)
    prompt = conversation.get_prompt(tokenizer)

    output = generate(model, tokenizer, prompt, generation_config)
    print(inp)
    print(output)
    print()
    print("==============================")
    print()

'''