# DPR-quanta
- This project tries to use DPR retrieval system on the quanta QA dataset(https://s3-us-west-2.amazonaws.com/pinafore-us-west-2/qanta-jmlr-datasets/qanta.train.2018.04.18.json). .
- The wikipedia dataset(https://s3-us-west-2.amazonaws.com/pinafore-us-west-2/qanta-jmlr-datasets/wikipedia/wiki_lookup.json) is used as a document set.
- As entire passage will be difficult for the DPR to process for generating embeddings, all the wikipedia articles are broken into passages of 200 words.
- Quanta dataset questions differs in the sense that each line of question might be related to different passages. Due to this the top retrieved passages were somewhat related to the problem statement but many a times it didn't exactly had the answer. 
- To solve the above problem an average of embeddings for each wikipedia article is taken and then the nearest neigbor search with respect to the questions is done. The averaging of embeddings for each wikipedia article increases the accuracy by 15-20%.
- Due to system limitations embeddings of only 1000 randomly selected wikipedia articles is generated and taken into consideration.

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

- Although, the accuracy of retrieved documents is not that great, however, the aim of DPR was to find positive passages with respect to the question, which it does quite efficiently. for example (for question having Napolean as the answer the top 5 retrieved documents are 'French_Revolution', 'July Revolution', 'Napoleanic Wars', 'Napolean', 'Louis_XVI')
-  Also, when a QA model is applied on the retrieved top 20 documents, most of the times the answer with highest confidence usually is the anser or it contains the actual answer of the question.



