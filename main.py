import sys
import os
import json
import re
from src.preprocessor import Preprocess
from src.rake import RAKE
import warnings
warnings.filterwarnings("ignore")  # ignore the re.split() warning


def clean_unicoded_text(unicoded_text):
	""" cleans and returns unicoded text """
	ascii_encoded_text = unicoded_text.encode('ascii','ignore')
	utf_text = ascii_encoded_text.decode('utf-8','ignore')
	cleaned_text = re.sub(r"[-'\"]", " ", utf_text)
	return cleaned_text


def main(text):
	cur_dir = (os.path.abspath(os.curdir))
	text = clean_unicoded_text(text)

	stop_words_path = os.path.join(cur_dir, "RAKE","datas","FoxStoplist.txt")
	set_phrases, phrases =Preprocess(text, stop_words_path).text_to_phrases()
	keywords_counter_obj = RAKE(text, phrases).start()
	keywords_response = [{'text': k.strip(), 'score': v} for k,v in keywords_counter_obj]

	return keywords_response


if __name__=="__main__":
	text = "Some text to extract keywords"
	main(text)