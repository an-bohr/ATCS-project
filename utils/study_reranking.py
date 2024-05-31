import json


dictionary1 = json.load(open('new_result/roberta-base-corrected.json',"r"))
dictionary2 = json.load(open('new_result/roberta-base.json',"r"))
for i in dictionary1.keys():
	for j in dictionary1[i][:10]:
		print("Corrected:", j[0])

	for j in dictionary2[i][:10]:
		print("Original:", j[0])