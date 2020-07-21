import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import tensorflow_text
import nltk
from IPython.display import HTML, display
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.stem import PorterStemmer,SnowballStemmer
from rank_bm25 import BM25Plus
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request

nltk.download('stopwords')
nltk.download('punkt')

stop_words = set(stopwords.words('english'))


ps = PorterStemmer()
sn = SnowballStemmer('english')



module = hub.load('https://tfhub.dev/google/universal-sentence-encoder-qa/3') ### Change path to local cwd if you have the downloaded .pb model


def angular_similarity(x,y):
  return (1 - (np.arccos(cosine_similarity(x, y)) / np.pi))


def preprocess(text):
  word_tokens = word_tokenize(text)
  filtered_sentence = [w for w in word_tokens if not w in stop_words] 

  stemmed_sentence = [sn.stem(w) for w in filtered_sentence]
  # stemmed_sentence = [ps.stem(w) for w in filtered_sentence]
    
  text = " ".join(filtered_sentence)

  return text


def return_top_n(zipped,n):
  x =  [r for s,r in sorted(zipped, key = lambda x: x[0])[::-1][:n]]
  return x
  

app = Flask(__name__)



@app.route('/get_response_form',methods=['GET','POST'])
def get_resp():

	if request.method == 'POST':         	
		
		sent = request.form["sent"]
		query = request.form["query"]
		weight1 = request.form["weight1"]
		weight2 = request.form["weight2"]
		n = request.form["n"]

		
		######
		if weight1 == "":
			weight1 = 0.5
		else:
			weight1 = float(weight1)

		if weight2 == "":
			weight2 = 0.5
		else:
			weight2 = float(weight2)
			
		if n=="":
			n = 3
		else:
			n = int(n)


		######
		sentences = sent.split(',')


		candidate_embeddings = module.signatures['response_encoder'](
	    	input=tf.constant(sentences),
	    	context=tf.constant(sentences))['outputs']

		query_embedding = module.signatures['question_encoder'](tf.constant([query]))['outputs'][0]
		similarities = angular_similarity([query_embedding],candidate_embeddings)
		score = similarities[0]   ###########  Ranker 1 - USEQA Angular #########




	#### BM25+ ####
		
		preprocessed_query = preprocess(query)
		preprocessed_sentences = [preprocess(sent) for sent in sentences]
		
		tokenized_corpus = [doc.split(" ") for doc in preprocessed_sentences]
		ranker = BM25Plus(tokenized_corpus)

		tokenized_query = preprocessed_query.split(" ")

		r2 = ranker.get_scores(tokenized_query)

		w1 = weight1
		w2 = weight2

		print("######################")
		print("weight one : " , w1)
		print("weight two : ", w2)
		print("####################")


		weighted_final = w1*score + w2*r2

		zipped = list(zip(weighted_final,sentences))

		resp1 = return_top_n(zipped,n)
		
		final = {"Query" : query,
			"result" : resp1}
		
		return(final)
	
	return '''<form method="POST">
                  	Query: <input type="text" name="query" size='50'><br><br>
			<label for="Candidates">Candidates:</label>
			<textarea id = "Candidates" rows="20" cols ="100" name="sent" placeholder="Enter all candidate strings here.."></textarea><br><br>
                  	USEQA_weight: <input type="number" placeholder="0.5" step="0.01" min="0" max="10" name="weight1"><br>
                  	BM25+_weight: <input type="number" placeholder="0.5" step="0.01" min="0" max="10" name="weight2"><br><br>
                  	Top_n_results: <input type="number" placeholder="3" name="n"><br>
                  	<input type="submit" value="Submit"><br>
                  </form>'''


if __name__ == '__main__':
   app.run(host= '0.0.0.0',debug = True)
