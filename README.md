# DPR-quanta
- This project tries to use DPR retrieval system on the [quanta] (https://s3-us-west-2.amazonaws.com/pinafore-us-west-2/qanta-jmlr-datasets/qanta.train.2018.04.18.json) QA dataset.
- The [wikipedia dataset](https://s3-us-west-2.amazonaws.com/pinafore-us-west-2/qanta-jmlr-datasets/wikipedia/wiki_lookup.json) is used as as a document set.
- As entire passage will be difficult for the DPR to process for generating embeddings, all the wikipedia articles are broken into passages of 200 words.
- Quanta dataset questions differs in the sense that each line of question might be related to different passages. Due to this the top retrieved passages were somewhat related to the problem statement but many a times it didn't exactly had the answer. 
- To solve the above problem an average of embeddings for each wikipedia article is taken and then the nearest neigbor search with respect to the questions is done. The averaging of embeddings for each wikipedia article increases the accuracy by 15-20%.
- Due to system limitations embeddings of only 1000 randomly selected wikipedia articles is generated and taken into consideration.

## Steps to run the code

Run the below commands in the terminal for running the code:
1. sudo apt install libomp-dev
2. python create_dataset.py
3. python generate_embeddings.py
4. python test.py

## Results



