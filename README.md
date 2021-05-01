# DPR-quanta
- This project tries to use the DPR retrieval system on the quanta QA dataset(https://s3-us-west-2.amazonaws.com/pinafore-us-west-2/qanta-jmlr-datasets/qanta.train.2018.04.18.json). 
- The Wikipedia dataset(https://s3-us-west-2.amazonaws.com/pinafore-us-west-2/qanta-jmlr-datasets/wikipedia/wiki_lookup.json) is used as a document set.
- All the Wikipedia articles are broken into passages of 200 words.
- Quanta dataset questions differ in the sense that each line of question might be related to different passages. Due to this, the top retrieved passages were somewhat related to the problem statement but many times it doesn't exactly belong to the answer page. 
- To solve the above problem an average of embeddings for each Wikipedia article is taken and then the nearest neighbor search with respect to the question is done. The averaging of embeddings for each Wikipedia article increases the accuracy by 10-15%.

## Steps to run the code

Run the below commands in the terminal for running the code:
1. sudo apt install libomp-dev
2. pip install -r requirements.txt
3. curl https://s3-us-west-2.amazonaws.com/pinafore-us-west-2/qanta-jmlr-datasets/qanta.train.2018.04.18.json > quanta.train.json
4. curl https://s3-us-west-2.amazonaws.com/pinafore-us-west-2/qanta-jmlr-datasets/wikipedia/wiki_lookup.json > wiki_lookup.json
5. python create_dataset.py
6. python generate_embeddings.py
7. python test.py

## Results

| Case | Accuracy |
| ------------------ | -------------------- |
| The answer page is in the top 1 retrieved documents | 42.6% |
| The answer page is in the top 5 retrieved documents | 61.7% |
| The answer page is in the top 10 retrieved documents | 68.9% |
| The answer page is in the top 20 retrieved documents | 76.7 %|

## Conclusion
- Although, the accuracy of retrieved documents is not that great, however, the aim of DPR was to find positive passages with respect to the question, which it does quite accurately.
- The passages/documents retrieved are usually having similarity with some part of the question and are quite realted to the actual answer/answer page.  For example (for question having Napolean as the answer the top 5 retrieved documents are 'French_Revolution', 'July Revolution', 'Napoleanic Wars', 'Napolean', 'Louis_XVI').
- For now accuracy is only considered when the document retrieved is same as the answer page, however many times when QA models are applied on passages of different documents correct answer is retrieved.
- When QA models( BertForQuestionAnswering, ElectraForQuestionAnswering, etc.) are applied on the retrieved top 20 documents, the answer that comes with the highest confidence is usually the actual answer or some part of it contains the actual answer.




