# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 2024

@author: Kay Hales

Purpose: Using OpenStates PluralPolicy API to scrape immigration bills
"""

import pyopenstates
pyopenstates.set_api_key('secret.py')

import pandas as pd

import time

# Fetch Bill Data
states = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID',
    'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS',
    'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK',
    'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV',
    'WI', 'WY'
]
# Years
years = [2012, 2016, 2020]




# Loop through each state and year, fetching immigration bills
def query_immigration_bills(state, year):
    """
    Fetches immigration-related bills for a given state and year.
    """
    print(f"Querying {state} for {year}...")
    
    # Start date for the year
    start_date = f'{year}-01-01'
    
    try:
        # Query bills created or updated since the start of the year
        bills = pyopenstates.search_bills(
            jurisdiction=state,
            q='immigration',
            created_since=start_date
        )
        
        # Wait 6 seconds before the next query
        time.sleep(6)
        
        return bills
    
    except Exception as e:
        print(f"Error querying {state} for {year}: {e}")
        return None  # Return None if there's an error, so we can skip the iteration

all_bills = []

for state in states:
    for year in years:
        try:
            bills = query_immigration_bills(state, year)
            
            # Skip if the query failed (returned None)
            if bills is not None:
                # Filter bills based on the year they were created
                filtered_bills = [bill for bill in bills if bill['created_at'].year == year]
                
                # Append the filtered bills to the list
                all_bills.extend(filtered_bills)
        
        except Exception as e:
            print(f"Unhandled error with {state} in {year}: {e}")
            
# Convert the list of bills to a DataFrame for analysis
bills_df = pd.DataFrame.from_dict(all_bills)
bills_df.head()
# Convert the list of bills to a DataFrame for analysis
bills_df = pd.DataFrame.from_dict(all_bills)

# Display the DataFrame
bills_df.head()
