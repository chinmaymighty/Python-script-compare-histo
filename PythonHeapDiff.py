import csv
import os
import glob

def load_baseline():
	baseline = {}
	global baseline_path
	baseline_path = input("Enter the baseline file path (inside ''): ");
	# baseline_path = '/Users/rchinmay/Documents/baseline.csv'
	# baseline_path = '/Users/rchinmay/Documents/Custom_Query/pages/Query_Command2.csv'
	with open(baseline_path) as f:
		csvr = csv.reader(f)
		header = next(csvr)
		global count
		count = int(next(csvr)[0])
		for row in csvr:
			baseline[row[0]] = row[1:3]
	return baseline

def add_data_to_baseline(data, baseline):
	global count
	global baseline_path
	for val in data:
		key = val[0]
		value = val[1:3]
		base = [0,0]
		if key in baseline:
			base = list(map(int, baseline[key]))
		base[0] *= count
		base[1] *= count
		base[0] += int(value[0])
		base[1] += int(value[1])
		base[0] /= (1+count)
		base[1] /= (1+count) 
		baseline[key] = base
	count += 1
	# print(baseline)
	sorted_total = sorted(baseline.items(), key = lambda x: (x[1][1], x[1][0]), reverse = True)
	with open(baseline_path, 'w') as f:
		csvr = csv.writer(f)
		csvr.writerow(['Class Name','Objects','Shallow Heap'])
		csvr.writerow([count])
		# csvr.writerows(sorted_total)
		for row in sorted_total:
			lis = [row[0], row[1][0], row[1][1]]
			csvr.writerow(lis)

if __name__ == '__main__':
	heap_filename = input("Enter the absolute path to heap_dump (inside ''): ")
	# heap_filename = '/Users/rchinmay/Documents/java_pid48008.hprof'
	# heap_filename = '/Users/rchinmay/Desktop/Parser/biggestHeap.hprof'
	if(heap_filename[-6:] != '.hprof'):
		print('Heap File name should end in ".hprof"')
		system.exit(-1)
	os.system('/Applications/mat.app/Contents/Eclipse/ParseHeapDump.sh '+heap_filename+' -command=histogram -format=csv -unzip org.eclipse.mat.api:query')
	csv_folder = heap_filename[:-6] + '_Query/pages'
	# print(csv_folder)
	filenames = glob.glob(csv_folder + '/*.csv')
	# print(filenames)
	all_data = []
	for file in filenames:
		with open(file, 'r') as f:
			csvr = csv.reader(f)
			header = next(csvr)
			# print(header)
			for row in csvr:
				all_data.append(row)
			# print(header)
	print("Length: ", len(all_data))
	baseline = {}
	baseline = load_baseline()
	print("Baseline: ");
	print(baseline)
	
	# sort baseline and all_data
	sorted_baseline = sorted(baseline.items(), key = lambda x: (x[1][1], x[1][0]), reverse = True)
	# all_data.sort(key = lambda x: (x[1][1], x[1][0]), reverse = True) -- Not necessary since input from mat is sorted

	#compare top n classes
	n = input("Enter the number of top classes to compare: ")
	# n = input()
	for i in range(min(n,len(all_data))):
		print(i+1 ,"th largest class by size in given hprof is: " ,all_data[i][0:3], ". Its baseline usage was: ", baseline.get(all_data[i][0], (0,0)), sep='')

	#Add data to baseline
	add_data_to_baseline(all_data, baseline)