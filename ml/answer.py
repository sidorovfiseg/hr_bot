import ml
from ml import model_answer, tokenizer_answer, model_embedding, model_answer_name, generation_config_answer
import heapq
import torch
from ml.preprocess import prepare_text


def embed_request(request):
    return model_embedding.encode(request, convert_to_tensor=True)

def find_top_similar_tensors_in_chapter(input_tensor, tensor_array, k = 1):
    heap = []
    for j, tensor in enumerate(tensor_array):
        cosine_distance = torch.cosine_similarity(input_tensor, tensor, dim=0)
        heapq.heappush(heap, (cosine_distance, (j)))

    top_k_indices = heapq.nlargest(k, heap, key=lambda x: x[0])

    return [indices for _, indices in top_k_indices]

def find_top_similar_tensors(input_tensor, tensor_array, k = 1):
    heap = []
    for i, sub_array in enumerate(tensor_array):
        for j, tensor in enumerate(sub_array):
            cosine_distance = torch.cosine_similarity(input_tensor, tensor, dim = 0)
            heapq.heappush(heap, (cosine_distance, (i, j)))

    top_k_indices = heapq.nlargest(k, heap, key=lambda x: x[0])

    return [indices for _, indices in top_k_indices]



def get_c(question):
    q = prepare_text(question)
    print(q)
    q = embed_request(q)
    k = find_top_similar_tensors(q, ml.embeds_data)
    r = k[0]
    x = r[0]
    y = r[1]
    print(ml.text_data[x][y])
    chapter = ml.text_data[x]
    return chapter

def get_answer(question):

    chapter = ' '.join(get_c(question))
    print(chapter)
    with open('promt.txt', encoding='utf-8') as f:
        promt = f.read()
        promt = promt.format(chapter, question)

    print('Постановка задачи : ', promt)

    data = tokenizer_answer(promt, return_tensors="pt")
    data = {k: v.to(model_answer.device) for k, v in data.items()}
    output_ids = model_answer.generate(
        **data,
        generation_config=generation_config_answer
    )[0]

    print("====================")
    print(tokenizer_answer.decode(output_ids.tolist()))