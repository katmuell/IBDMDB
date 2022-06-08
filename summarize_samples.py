#Load modules
import os.path
import pandas as pd
from csv import writer
import glob
import re
import sys
import numpy as np

#Define paths
output_file = 'summarized_samples.txt'
input_path = sys.argv[1] + '*.abundances'	#input the folder that your strainR results are in when you call this script (ie. /work/kdm65/project_folder/results )
listing = glob.glob(input_path)

header_pass = 0
#Create the header of the summary file if it doesn't exist yet
if os.path.isfile(output_file):
	header_pass = 1
else:
	header = pd.DataFrame(columns = ["SampleID", "AMIa", "AMIb", "AMII", "AMIII", "AMIV", "AMV", "AMVI-muc2"])	#This assumes that you're using the 7 strain database that Lauren put together. If not, you'll need to update the list with your strain names.
	header.to_csv(output_file, index = False)
	header_pass = 1

for filename in listing:
	if header_pass == 1:
		#Calculate median log10FUKM for all strains
		data_to_summarize = pd.read_csv(filename, delimiter = "\t")
		pd.set_option('mode.use_inf_as_na', True)
		with np.errstate(divide='ignore'):	#log10 in the next step will probably return errors for diving by zero. But we deal with that after, so I'm turning the error message off for this one calculation.
			data_to_summarize["log10FUKM"] = np.log10(data_to_summarize["FUKM"]).dropna(how="any")		#Calculate log10FUKM and drop the ones that couldn't be calculated because the FUKM was zero. This is what the strainR graphs do as well.
		medians = data_to_summarize[["StrainID", "log10FUKM"]].groupby("StrainID").median().reset_index()	#Calculate median log10FUKM of each phylogroup
		SampleID_pattern = "\S*\/(.*?)\.abundances"
		SampleID = re.search(SampleID_pattern, filename).group()

		#If strain appears in the strainR results file, grab the median FUKM value. Otherwise, assign abundance as zero. Do in order of strains 1-7 to keep the output consistent.
		strains_desired = ["AMIa", "AMIb", "AMII", "AMIII", "AMIV", "AMV", "AMVI-muc2"]		#The strains we expect to have/what we included in the reference
		strains_available = pd.unique(medians['StrainID'])	#The strains that actually appear in the sample being summarized

		abundances_list = [SampleID]
		for s in strains_desired:
			dataframe_label = str(s)
			if s in strains_available:
				abundance = medians[medians['StrainID'] == s].iloc[0]["log10FUKM"]
			else:
				abundance = 0
			abundances_list.append(abundance)	#Generate a row for the abundance of each strain in the sample being summarized

		#Write sample abundances to output file
		with open(output_file, 'a+', newline='') as write_obj:		#Add the abundance row for the sample being summaried to the output dataframe
			csv_writer = writer(write_obj)
			csv_writer.writerow(abundances_list)

	else:
		print("Error. No file containing header found")		#This shouldn't happen
