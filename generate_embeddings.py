from transformers import DPRContextEncoder, DPRContextEncoderTokenizer, DPRContextEncoderTokenizerFast, DPRConfig
import torch
torch.set_grad_enabled(False)
ctx_encoder = DPRContextEncoder.from_pretrained("facebook/dpr-ctx_encoder-single-nq-base")
ctx_tokenizer = DPRContextEncoderTokenizerFast.from_pretrained("facebook/dpr-ctx_encoder-single-nq-base")

from transformers import DPRQuestionEncoder, DPRQuestionEncoderTokenizer, DPRQuestionEncoderTokenizerFast
q_encoder = DPRQuestionEncoder.from_pretrained("facebook/dpr-question_encoder-single-nq-base")
q_tokenizer = DPRQuestionEncoderTokenizerFast.from_pretrained("facebook/dpr-question_encoder-single-nq-base")

from datasets import load_dataset
ds = load_dataset('json', data_files='quanta_psgs.json',field='data')
ds_with_embeddings = ds.map(lambda example: {'embeddings': ctx_encoder(**ctx_tokenizer(example["text"], return_tensors="pt", max_length=512, truncation=True))[0][0].numpy()})
ds_with_embeddings['train'].add_faiss_index(column='embeddings')
ds_with_embeddings['train'].save_faiss_index('embeddings', 'quanta_psgs.faiss')

map_embeddings = {}
count = 1
for i in range (0, len(ds_with_embeddings['train'])):
    title = ds_with_embeddings['train'][i]['title']
    if ds_with_embeddings['train'][i]['title'] in map_embeddings.keys():

        for e in range(0, len(map_embeddings[title])):
            map_embeddings[title][e] = (ds_with_embeddings['train'][i]['embeddings'][e] + map_embeddings[title][e]*(count))/(count +  1)
        
        count = count + 1
    else:
        map_embeddings[title] = ds_with_embeddings['train'][i]['embeddings']
        count = 1
#     print(count)

ds_with_embeddings_avg = ds1.map(lambda example: {'embeddings': map_embeddings[example['title']]})
ds_with_embeddings_avg['train'].add_faiss_index(column='embeddings')
ds_with_embeddings_avg['train'].save_faiss_index('embeddings', 'quanta_psgs_avg.faiss')
