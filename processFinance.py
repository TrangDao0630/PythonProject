import os
import pandas as pd
    
def process_file(data, filename):
    # Add your processing logic here
    print("Processing file: " ,  filename)
    # For example, you can check the filename and apply different processing
    if 'activity' in filename:
        # Process amex data
        data = data.rename(columns={'Card Member': 'Type' })
        data['Amount'] = data['Amount'] * -1
        data['Category'] = data['Description'].apply(lambda x: getCategoryFromDescription(x) )
    elif ('Chase8248' in filename) or ('Chase3775' in filename):
        # Process chase bank account data
        data['Category'] = data['Description'].apply(lambda x: getCategoryFromDescription(x) )
        data['Amount'] = data['Amount'] * -1
        data.loc[data['Description'].str.contains('Payment to Chase card ending in 8788'), 'Type'] = 'TRANG DAO'
        data = data.rename(columns={ 'Posting Date': "Date"})
        # print(data.keys())
    elif 'Chase' in filename:
        # Process chase credit card data
        data = data.rename(columns={'Transaction Date': 'Date'})
    elif 'Date range' in filename:
        # citi bank credit card
        data['Debit'] = data['Debit'].fillna(0) * -1
        data['Credit'] = data['Credit'].fillna(0) * -1
        data['Amount'] = data['Debit'] + data['Credit']
        data['Category'] = data['Description'].apply(lambda x: getCategoryFromDescription(x) )
    return data

def getCategoryFromDescription(description):
    print("here is the description" , description)
    if 'Wealthfront' in description:
        return 'ACCT_XFER'
    elif 'PAYROLL' in description:
        return 'income'
    elif 'COINBASE INC' in description:
        return 'invest'
    elif 'Uplift' in description:
        return 'Entertainment'
    elif 'Zelle payment from MENGYUE LIAO' in description:
        return 'Bills & Utilities'
    elif 'TEMU.COM' in description:
        return 'Shopping'
    elif 'COSTO GAS' in description:
        return 'Gas'
    elif 'COSTCO WHSE' in description:
        return 'Groceries'
    elif "Market Square" in description:
        return 'House'
    return ''

def main(directory):
    combined_data = pd.DataFrame()

    for filename in os.listdir(directory):
        # read file
        if 'results' not in filename and (filename.endswith('.csv') or filename.endswith('.CSV')):
            print('starting processing for ' + filename)
            file_path = os.path.join(directory, filename)
            data = pd.read_csv(file_path, index_col=False)

            # Process each file based on its filename
            data = process_file(data, filename)

            # Combine the data
            combined_data = pd.concat([combined_data, data], ignore_index=True)
        print('done processing for ' + filename + '\n')
    # Save the combined data to a new CSV file
    combined_data = combined_data[~combined_data['Description'].str.contains('AUTOPAY')]
    combined_data = combined_data[~combined_data['Description'].str.contains('AUTOMATIC PAYMENT')]
    print("Saving combined data")
    combined_data = combined_data.drop(columns=['Status', 'Member Name', 'Account #', 'Memo', 'Post Date', 'Balance', 'Check or Slip #', 'Debit', 'Credit', 'Details'])
    desired_order = ['Date', 'Description', 'Category', 'Type', 'Amount']
    combined_data = combined_data[desired_order]
    combined_data.to_csv(os.path.join(directory, 'results.csv'), index=False)

if __name__ == "__main__":
    # directory = input("Enter the directory path: ")
    # print(directory)
    # main(directory)
    activitycsv = input("Enter the directory path: ")
    print(activitycsv)
    main(activitycsv)
 
 