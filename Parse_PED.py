# Parse through a PED file and count the number of perfect/imperfect families

import pandas as pd
import argparse
import os.path

def is_valid_file(x):
        if not os.path.exists(x):
                raise argparse.ArgumentTypeError("{0} does not exist".format(x))        
        return x

parser = argparse.ArgumentParser(description="Choose PED file.")  
parser.add_argument("-f", "--input_file", dest="filename", required=True, type=is_valid_file, help="input file.", metavar="FILE")
args = parser.parse_args()

file = args.filename

content = []
perf_count = 0
imp_count = 0
current_count = 0
ind_ped = {}
#ind_ID (key) : sex(0 or 1) | FamID | father | mother
fam_ped = {}
#fam_ID (key) : fam_count
child_ped = {}
#child_ID (key) : father | mother | FamID
 
with open(file) as f:
	#read file and put into list
	for line in f:
		content.append(line.strip().split())
	#intialize ind dict and fam dict
	#remove the first line
	content.pop(0)
	for i in content:
		#add to dict
		new_ped = {str(i[1]):[ str(i[4]),str(i[0]),str(i[2]),str(i[3])]}
		ind_ped.update(new_ped)
			
		#check if it's a child
		if (int(i[2]) != 0 and int(i[3]) != 0):
			new_child = {str(i[1]): [str(i[2]), str(i[3]), str(i[0])]}
			child_ped.update(new_child)
		if(str(i[0]) in fam_ped.keys()):
			curr_count = fam_ped.get(str(i[0]),0)
			fam_ped[str(i[0])] =  curr_count + 1
		
		else:
			new_fam = {str(i[0]):1}
			fam_ped.update(new_fam)
	for i in fam_ped:
		print(fam_ped[i])
	#use family member count to determine completness of pedigree
	for i in fam_ped:
		if(int(fam_ped[i]) < 3):
			#print("Family ID: " + i + " has incomplete family pedigree.")
			imp_count = imp_count + 1	
		else:
			#print("Family ID: " + i + " has enough people for family pedigree.")
			perf_count = perf_count + 1

 	# --- something wrong with counting imp and perf count below ---
	# need to check for sex of parents in complete fam			
	for i in fam_ped:
		if (fam_ped[i] > 2):
			mother = 0
			father = 0

			for j in ind_ped:
				if ind_ped[j][1] == i :		
					if (int(i[2]) != 0 and int(i[3]) != 0):
						#print(ind_ped[j][0])
						#print(j)
						
						if (ind_ped[j][0] == 1):
							father = int(j)
						#print(j)
						#print(father)
						if (ind_ped[j][0] == 2):
							mother = int(j)
						
			for k in child_ped:
				#print(child_ped[k])
				#check if the parents of the child are actually the parent 
				#same family id but diff parents
				#print(child_ped[k][0])
				if child_ped[k][2] == i:
					if child_ped[k][0] != father or child_ped[k][1] != mother: 
					#print("parent mismatch in family")
						perf_count = perf_count - 1
						imp_count = imp_count + 1
						#print(father)
						#print(mother)					
						#check their sexes and discount overlap
						"""
						if ind_ped[father] != 1 or ind_ped[mother] != 2:
							if child_ped[k][0] != father or child_ped[k][1] != mother:
								continue
							else:
								print("parent sex mismatch")
								perf_count = perf_count - 1
								imp_count = imp_count + 1
						  """
	print("Perfect ped count: " + str(perf_count))
	print("Imperfect ped count: " + str(imp_count))
			
