
if __name__ == "__main__": 

# # Credit Transaction Problem
	## Clean the Data before processing (Pre-processing) ##
	## Calculate the total spending by credit card ##
	## How much was spend at WW GRAINER, WM SUPERCENTER & GROCERY STORES ##


	from pandas import Series, DataFrame
	import pandas as pd
	import numpy as np

	CDD = pd.read_csv('res_purchase_2014.csv',index_col=['Year-Month'])
	CDD

	# type(CDD)

	y = lambda x: str(x)
	CDD["Amount"] = CDD["Amount"].apply(y)    # Convert to string first


	f = lambda x: x.replace('$','').replace(' zero','').replace(')','').replace('(','-')  # Cleaning the Amount column
	CDD["Amount"] = CDD["Amount"].apply(f)
	CDD["Amount"] = pd.to_numeric(CDD["Amount"])        # Converting back to numeric form after cleaning

	Total_spending = sum(CDD.Amount)
	WW_GRAINGER_spending = sum(CDD.Amount[CDD.Vendor.str.contains('WW GRAINGER')])            # using contains as there were variations of the vendor name
	WM_SUPERCENTER_spending = sum(CDD.Amount[CDD.Vendor.str.contains('WM SUPERCENTER')])
	WW_GROCERY_spending = sum(CDD.Amount[CDD['Merchant Category Code (MCC)'].str.contains('GROCERY STORES')])

	print("Total Amount Spent: $", + round(Total_spending))
	print("Spent at  WW GRAINGER: $", + round(WW_GRAINGER_spending))
	print("Spent at  WM SUPERCENTER: $", + round(WM_SUPERCENTER_spending))
	print("Spent at  GROCERY STORES: $", + round(WW_GROCERY_spending))


	# # Credit Rating 
	## Perform Data Munging & Data Cleaning ##
	## Statistical approach to analyze Balance Sheet information along with rating data ##
	## Calculate the rating frequency for companies ending with 'CO'
	
	# BalanceSheet Data
	BalanceSheet = pd.read_excel('Energy.xlsx', index_col = 1)
	
	# Credit Ratings Data
	Ratings = pd.read_excel('EnergyRating.xlsx', index_col = 4)
	
	from numpy import nan as NA

	BalanceSheet = BalanceSheet.dropna(axis = 1,thresh = 85)   #70 columns dropped, with at least 10% non-NA values -> 844*.10 = 85

	Ratings = Ratings.dropna(axis = 1,thresh = 252) #1 column dropped, with at least 10% non-NA values -> 2522*.10 = 252
	Ratings

	# Replace NAN with mean of the column
	BalanceSheet = BalanceSheet.fillna(BalanceSheet.mean())

	Ratings = Ratings.fillna(Ratings.mean())

	# Checking datatypes of the columns of the df
	BalanceSheet.dtypes

	# Checking object datatypes columns of the df
	BalanceSheet.select_dtypes(include=[object,'category']).columns

	not_tobe_normalized = ['Data Date','Global Company Key','Fiscal Year','Fiscal Quarter','Fiscal Year-end Month','CIK Number','Stock Exchange Code']

	BalanceSheet = BalanceSheet.apply(lambda x: x if x.name in not_tobe_normalized else (x - x.min())/(x.max() - x.min()) if x.dtypes!='object' else x)


	# Correlation Matrix
	ret = BalanceSheet[['Current Assets - Other - Total','Current Assets - Total','Other Long-term Assets','Assets Netting & Other Adjustments']]
	print(ret.corr())


	# CO column addition
	match = lambda x: 'CORP'if 'CORP' in x else 'CO' if 'CO' in x else 'INC' if 'INC' in x else x
	BalanceSheet['CO'] = BalanceSheet['Company Name'].map(lambda x: match(x))


	# Merge the two df
	Matched=pd.merge(BalanceSheet,Ratings,on=['Data Date','Global Company Key'],how='inner')

	# Mapping with Credit Ratings
	credit_rating={'AAA':0,'AA+':1,'AA':2,'AA-':3,'A+':4,'A':5,'A-':6,'BBB+':7,'BBB':8,'BBB-':9,'BB+':10,'BB':11,'others':12}
	Matched['Rate']=Matched['S&P Domestic Long Term Issuer Credit Rating'].map(credit_rating)
	Matched

	# Computing frequency of each Credit Rating for 'CO' Companies
	freq=Matched.Rate[Matched['CO']=='CO'].value_counts()
	reversed_credit_rating = {value : key for (key, value) in credit_rating.items()}
	freq.index=freq.index.map(reversed_credit_rating)
	print(freq)


	# Export to csv
	Matched.to_csv('Credit Rating freq.csv')

