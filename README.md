step1: install pandas and dash using command -> pip install requirements.txt

step2: open python/anaconda shell and cd to required directory. Both the py files should be in this directory. 

step3: use command -> python app-dash-part1.py , open the webpage with the link obtained. Browse a csv file (Real estate.csv).

step4: go to python shell and press ctrl+C to stop this server. This *part1.py file will call team-2 function to clean the data. A csv file named cleaned_df.csv will be saved in working directory.

step5: use command -> python app-dash-part2.py, refresh the webpage opened earlier to see the output. This code reads the cleaned_df.csv and will ask user to select x & y variables. It also has option of scatter plot between any two variables. 

The output from above code will a pandas dataframe, having X & y variables. Last column will be y variable. Thus other team can use this ordered_df for their further processing.
