import ml
from ml import model_answer, tokenizer_answer, model_embedding, model_answer_name, generation_config_answer
import heapq
import torch
from ml.preprocess import prepare_text

def embed_request(request):
    return model_embedding.encode(request, convert_to_tensor = True)


def find_top_similar_tensors(input_tensor, tensor_array, k = 5):
    result = []
    for sub_array in tensor_array:
        cosine_distances = [torch.cosine_similarity(input_tensor, tensor, dim = 0) for tensor in sub_array]
        max_cosine_distance = max(cosine_distances)
        result.append(max_cosine_distance)

    top_k_indices = sorted(range(len(result)), key = lambda i: result[i], reverse = True)[ : k]
    return [(index, result[index]) for index in top_k_indices]


def get_answer(question, chapter):

    with open('..\promt.txt', encoding='utf-8') as f:
        promt = f.read()
        promt = promt.format(chapter, question)

   # print('Постановка задачи : ', promt)

    data = tokenizer_answer(promt, return_tensors="pt")
    data = {k: v.to(model_answer.device) for k, v in data.items()}
    output_ids = model_answer.generate(
        **data,
        generation_config=generation_config_answer
    )[0]

    print("====================")
    return tokenizer_answer.decode(output_ids.tolist())

def get_c(question):
    print(f"Вопрос : [{question}]")
    q = prepare_text(question)
    print(q)
    q = embed_request(q)

    ind_ = find_top_similar_tensors(q, ml.embeds_data)

    for (i, j) in ind_:
        print(f"{ml.text_data[i]} \n score : {j}")

    print("====================")
    h = get_answer(question, ml.text_data[ind_[0][0]])
    print(h)
    print("====================")




if __name__ == '__main__':
    print(ml.text_data)
    q1 = 'Какие бывают типы встреч?'
    q2 = 'Материальная помощь сотрудникам?'
    q3 = 'В чем заключается принцип результативности?'
    q4 = 'Наступление Вагнер под Соледаром?'
    q5 = 'Как победить черную рассу?'
    #q2 = 'Как компания "Смартократия" поддерживает неравнодушие и свободу среди своих сотрудников и клиентов, и как это влияет на проекты и результаты компании?'
    #q3 = 'Каким образом Лидлинк определяет формат проведения встречи - очный офлайн, онлайн или заочно? И какие факторы влияют на это решение?'
    #q4 = 'При каких условиях и ситуациях рекомендуется проводить встречи в заочном формате, а при каких рекомендуется проводить встречи очно или онлайн?'
    #q5 = 'Что определяет Кодекс Смартократии, и как он регулирует основные понятия, правила и процессы управления в Группе Компаний Smart Consulting?'
    #q6 = 'Каким образом регулируется участие сотрудников на встречах, где используется информация, доступ к которой ограничен законодательством Российской Федерации?'
    #q7 = 'Какие критерии и процедуры определяются для одобрения участия сотрудников на встречах ограниченного доступа, и кто является организатором таких встреч?'
    #q8 = 'Каким образом каждый сотрудник фиксирует свои усилия в рамках работы, и какие категории используются для такой фиксации?'
    #q9 = 'Какие информационные системы используются в ГК для фиксации усилий сотрудников, и как эти системы помогают отслеживать активности в разрезе кругов, ролей, обязательств и проектов?'
    #q10 = 'Что определяет Кодекс Смартократии, и как он регулирует основные понятия, правила и процессы управления в Группе Компаний Smart Consulting?'
    #q3 = 'Каким образом Лидлинк определяет формат проведения встречи - очный офлайн, онлайн или заочно? И какие факторы влияют на это решение?'
    #q4 = 'При каких условиях и ситуациях рекомендуется проводить встречи в заочном формате, а при каких рекомендуется проводить встречи очно или онлайн?'
    get_c(q1)
    get_c(q2)
    get_c(q3)
    get_c(q4)
    get_c(q5)
    #get_c(q6)
    #get_c(q7)
    #get_c(q8)
    #get_c(q9)
    #get_c(q10)

