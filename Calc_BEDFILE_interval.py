# Simple code that returns the intervals of given BEDFILE 

import pandas as pd
import argparse
import os.path

def is_valid_file(x):
	if not os.path.exists(x):
		raise argparse.ArgumentTypeError("{0} does not exist".format(x))	
	return x

parser = argparse.ArgumentParser(description="Choose interval value.")	
parser.add_argument("-v", "--interval_value", type=int, help="type the interval value.")
parser.add_argument("-f", "--input_file", dest="filename", required=True, type=is_valid_file, help="input file.", metavar="FILE")
args = parser.parse_args()

file = args.filename

content = []
interval_val = args.interval_value
result = [] 
current_amount=0
file_num = 0
with open(file) as f:
	#takes 		
	for line in f:
		content.append(line.strip().split())
	
	for i in content:
		diff_count = int(i[2]) - int(i[1])
		previous_count = current_amount
		current_amount = current_amount + diff_count
		
		if (interval_val > current_amount):
			result_line = i[0] + " " + i[1] + " " + i[2]
			result.append(result_line.strip().split())
			if i == content[len(content)-1]:										 
				with open("/home/shl457/arzoo_prac/results/"+str(file_num)+"result.txt", "w") as f:
					file_num = file_num + 1
					for j in result:
						f.write(j[0]+":"+j[1]+"-"+j[2]+"\n")	
				result.clear()
				current_amount = 0			

		if (interval_val == current_amount):
			result_line = i[0] + " " + i[1] + " " + i[2]
			result.append(result_line.strip().split())

			with open("/home/shl457/arzoo_prac/results/"+str(file_num)+"result.txt", "w") as f:
				file_num = file_num + 1
				for i in result:
					f.write(i[0]+":"+i[1]+"-"+i[2]+"\n")
				result.clear()
			current_amount = 0

		if (interval_val < current_amount):
			break_value = interval_val - previous_count
			result_line = i[0] + " " + i[1] + " " + str(int(i[1])+break_value)
			result.append(result_line.strip().split())
			
			with open("/home/shl457/arzoo_prac/results/"+str(file_num)+"result.txt", "w") as f:
				file_num = file_num + 1
				for j in result:
					f.write(j[0]+":"+j[1]+"-"+j[2]+"\n")
			
			result.clear()
			current_amount = 0

			place_hold = int(i[1]) + break_value
 
			if int(i[2]) - place_hold > interval_val: #put while loop below
				while int(i[2]) - place_hold > interval_val: 
					result_line = i[0] + " " + str(place_hold) + " " + str(place_hold + interval_val)
					result.append(result_line.strip().split())
					with open("/home/shl457/arzoo_prac/results/"+str(file_num)+"result.txt", "w") as f:
						file_num = file_num + 1
						for j in result:
							f.write(j[0]+":"+j[1]+"-"+j[2]+"\n")
					result.clear()
					place_hold = place_hold + interval_val

			if int(i[2]) - place_hold < interval_val:	
				result_line = i[0] + " " + str(int(place_hold)) + " " + i[2]
				result.append(result_line.strip().split())
				current_amount = int(i[2]) - place_hold
				if i == content[len(content)-1]:										 
					with open("/home/shl457/arzoo_prac/results/"+str(file_num)+"result.txt", "w") as f:
						file_num = file_num + 1
						for j in result:
							f.write(j[0]+":"+j[1]+"-"+j[2]+"\n")	
					result.clear()
					current_amount = 0			

			if int(i[2]) - place_hold == interval_val:
				result_line = i[0] + " " + str(place_hold) + " " + i[2]
				result.append(result_line.strip().split())
				with open("/home/shl457/arzoo_prac/results/"+str(file_num)+"result.txt", "w") as f:
					file_num = file_num + 1
					for j in result:
						f.write(j[0]+":"+j[1]+"-"+j[2]+"\n")
				result.clear()
