from flask import Flask,render_template,request
from Main import get_tweets
from Main_offline import get_tweets as get_tweets_offline
import pickle
import os
import csv

app=Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")
@app.route('/search')
def search():
	if request.method=='GET':
		if(request.args.get('searchbox')):
			searchbox=request.args.get('searchbox')
			get_tweets(searchbox)
			with open("akriti_pie_data.pickle",'rb') as f:
				count=pickle.load(f)
			return render_template("result.html",count=count)
	return render_template("search.html")
@app.route('/offline')
def offline():
	get_tweets_offline('offline_data.csv')
	with open("akriti_pie_data.pickle",'rb') as f:
		count=pickle.load(f)
	return render_template("result.html",count=count)

@app.route('/test')
def test():
	result_path=get_tweets_offline('test_dataset.csv')
	with open("akriti_pie_data.pickle",'rb') as f:
		count=pickle.load(f)
	path=r".\dataset"
	extract_file_path = os.path.join(path,'test_dataset.csv')
	with open(extract_file_path,'r',encoding='utf-8') as extract_file:
		sentiments=[]
		csv_reader = csv.reader(extract_file)
		for line in csv_reader:
			sentiments.append(line[0])
	with open(result_path,'r',encoding='utf-8') as csv_file:
		predicted_sentiments=[]
		csv_reader = csv.reader(csv_file)
		next(csv_reader)
		for line in csv_reader:
			predicted_sentiments.append(line[2])
	popo=0
	pong=0
	ponu=0
	ngpo=0
	ngng=0
	ngnu=0
	nupo=0
	nung=0
	nunu=0
	for i in range(len(sentiments)):
		if sentiments[i]=='positive' and predicted_sentiments[i]=='positive':
			popo+=1
		if sentiments[i]=='positive' and predicted_sentiments[i]=='negative':
			pong+=1
		if sentiments[i]=='positive' and predicted_sentiments[i]=='neutral':
			ponu+=1
		if sentiments[i]=='negative' and predicted_sentiments[i]=='positive':
			ngpo+=1
		if sentiments[i]=='negative' and predicted_sentiments[i]=='negative':
			ngng+=1
		if sentiments[i]=='negative' and predicted_sentiments[i]=='neutral':
			ngnu+=1
		if sentiments[i]=='neutral' and predicted_sentiments[i]=='positive':
			nupo+=1
		if sentiments[i]=='neutral' and predicted_sentiments[i]=='negative':
			nung+=1
		if sentiments[i]=='neutral' and predicted_sentiments[i]=='neutral':
			nunu+=1
	tp_po= popo
	tp_ng=ngng
	tp_nu=nunu
	fp_po=pong+ponu
	fp_ng=ngpo+ngnu
	fp_nu=nupo+nung
	fn_po=ngpo+nupo
	fn_ng=pong+nung
	fn_nu=ponu+ngnu
	precision_po = float(tp_po)/(tp_po+fp_po)
	precision_ng = float(tp_ng)/(tp_ng+fp_ng)
	precision_nu = float(tp_nu)/(tp_nu+fp_nu)
	recall_po = float(tp_po)/(tp_po+fn_po)
	recall_ng = float(tp_ng)/(tp_ng+fn_ng)
	recall_nu = float(tp_nu)/(tp_nu+fn_nu)
	precision= (precision_po+precision_ng+precision_nu)/3.0
	recall = (recall_nu+recall_po+recall_ng)/3.0
	fscore= 2.0*precision*recall/(precision+recall)
	total=len(sentiments)
	accuracy=(popo+ngng+nunu)/float(total)
	return render_template("result.html",count=count,result=[accuracy,precision,recall,fscore],data=[popo,pong,ponu, ngpo, ngng,ngnu, nupo, nung, nunu])

if __name__ == '__main__':
	app.run(debug=True)