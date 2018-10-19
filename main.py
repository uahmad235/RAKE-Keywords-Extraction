import sys
import os
import json

from .RAKE_1_RegExSplit_Copy import *
from .RAKE_2_Cooccur_Copy import *
from collections import Counter
import warnings
warnings.filterwarnings("ignore")  # ignore the re.split() warning


# If you want to modify an iterable inside a loop based on its iterator you should use a deep copy of it.


def clean_unicoded_text(unicoded_text):
	""" cleans and returns unicoded text """
	ascii_encoded_text = unicoded_text.encode('ascii','ignore')
	utf_text = ascii_encoded_text.decode('utf-8','ignore')
	cleaned_text = re.sub(r"[-'\"]", " ", utf_text)

	return cleaned_text

# def keywords_post_process()

def main(text):
	# return "Working  in RAKE.main()"
	# try:
	# text = ""
	# text = sys.argv[1]  # argument passed as text from node
	# print(text)

	cur_dir = (os.path.abspath(os.curdir))
	
	# # next_dir = "//datas//textfile.txt"
	# joined_path = os.path.join(cur_dir, "RAKE","datas","textfile.txt")
	# with open(joined_path,'r', encoding="utf-8", errors ="strict") as f:
	# 	for line in f:
	# 		text += " " +(line.strip())

	text = clean_unicoded_text(text)

	stop_words_path = os.path.join(cur_dir, "RAKE","datas","FoxStoplist.txt")
	set_phrases, phrases =Preprocess(text, stop_words_path).text_to_phrases()
	keywords_counter_obj = RAKE(text, phrases).start()

	# most_common = keywords_counter_obj()

	keywords_response = [{'text': k.strip(), 'score': v} for k,v in keywords_counter_obj]

	# return (json.dumps(keywords_response))
	return keywords_response
	# sys.stdout.write(keywords_response.toString())

	except Exception as err:
		# sys.stderr.write(err)
		raise Exception(err)

if __name__=="__main__":
	text = "Some text to extract keywords"
	main(text)