from transformers import DPRQuestionEncoder, DPRQuestionEncoderTokenizer, DPRQuestionEncoderTokenizerFast
import torch
from datasets import load_dataset
from statistics import mode
import json

torch.set_grad_enabled(False)

q_encoder = DPRQuestionEncoder.from_pretrained("facebook/dpr-question_encoder-single-nq-base")
q_tokenizer = DPRQuestionEncoderTokenizerFast.from_pretrained("facebook/dpr-question_encoder-single-nq-base")

f = open('quanta_questions.json')
questions_list = json.load(f)

page_in_top1 = 0
page_in_top5 = 0
page_in_top10 = 0
page_in_top20 = 0

ds_with_embeddings_avg = load_dataset('json', data_files='quanta_psgs.json',field='data')
ds_with_embeddings_avg['train'].load_faiss_index('embeddings', 'faiss_index/quanta_psgs_avg.faiss')

no_of_test_questions = 500

for i in range(0, no_of_test_questions):

    question = questions_list[i]['text']
    question_embedding = q_encoder(**q_tokenizer(question, return_tensors="pt"))[0][0].numpy()
    scores, retrieved_examples = ds_with_embeddings_avg['train'].get_nearest_examples('embeddings', question_embedding, k=500)
    
    top1_doc = []
    top5_doc = []
    top10_doc = []
    top20_doc = []

    for j in range(0, len(retrieved_examples)):
        
        if retrieved_examples['title'][j].lower() not in top1_doc and len(top1_doc) != 1:
            top1_doc.append(retrieved_examples['title'][j].lower())       

        if retrieved_examples['title'][j].lower() not in top5_doc and len(top5_doc) != 5:
            top5_doc.append(retrieved_examples['title'][j].lower())
        
        if retrieved_examples['title'][j].lower() not in top10_doc and len(top10_doc) != 10:
            top10_doc.append(retrieved_examples['title'][j].lower())
           
        if retrieved_examples['title'][j].lower() not in top20_doc and len(top20_doc) != 20:
            top20_doc.append(retrieved_examples['title'][j].lower())
        
        if(len(top20_doc) == 20):
            break
    
    if questions_list[i]['page'].lower() in top1_doc:
        page_in_top1 = page_in_top1 + 1

    if questions_list[i]['page'].lower() in top5_doc:
        page_in_top5 = page_in_top5 + 1
    
    if questions_list[i]['page'].lower() in top10_doc:
        page_in_top10 = page_in_top10 + 1
        
    if questions_list[i]['page'].lower() in top20_doc:
        page_in_top20 = page_in_top20 + 1
        
    print('Question: \n',  questions_list[i]['text'])
    print('Top 5 Retrieved Documents are: \n', top5_doc )
    print('The correct Document is :', questions_list[i]['page'])
    print('-----------------------------------------------------------------------------------------------------------------------------------------------------------------------')

print('Accuracy that the correct document is present in top 1 retrieved Documents: ',page_in_top1/no_of_test_questions )
print('Accuracy that the correct document is present in top 5 retrieved Documents: ',page_in_top5/no_of_test_questions )
print('Accuracy that the correct document is present in top 10 retrieved Documents: ',page_in_top10/no_of_test_questions )
print('Accuracy that the correct document is present in top 10 retrieved Documents: ',page_in_top20/no_of_test_questions )
