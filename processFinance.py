from io import StringIO
import os
import pandas as pd
    
def process_file(data, filename):
    print("Processing file: " ,  filename)
        # Process BOA data
    if 'stmt' in filename:  
        # Rename columns to match transaction data format
        data = data.rename(columns={'Running Bal.': 'Running Bal.'})
        data['Category'] = data['Description'].apply(lambda x: getCategoryFromDescription(x))
    # For example, you can check the filename and apply different processing
    elif 'activity' in filename:
        # Process amex data
        data['Amount'] = data['Amount'] * -1
        data['Category'] = data['Description'].apply(lambda x: getCategoryFromDescription(x) )
    elif 'Chase8788' in filename:
        # Process chase credit card data
        data = data.rename(columns={'Transaction Date': 'Date'})
        data['Category'] = data['Description'].apply(lambda x: getCategoryFromDescription(x) )

    return data

def getCategoryFromDescription(description):
    print("here is the description" , description)
    if 'AplPay' in description:
        return 'Food'
    elif 'CHE' in description:
        return 'Food'
    elif 'STARBUCKS' in description:
        return 'Food'
    elif 'BAMBU' in description:
        return 'Food'
    elif 'CSJ' in description:
        return 'Mis'
    elif 'USPS' in description:
        return 'Mis'
    elif 'WEPA' in description:
        return 'Mis'
    elif 'Mai' in description:
        return 'Food'
    elif 'VENMO' in description:
        return 'Food'
    elif 'Check' in description:
        return 'Tax'
    elif 'APPLE' in description:
        return 'Bills'
    return ''

def main(directory) :
    combined_data = pd.DataFrame()
    for filename in os.listdir(directory) :
        #read file
        if 'results' not in filename and (filename.endswith('.csv') or filename.endswith('.CSV')) :
            print('starting processing for ' + filename)
            file_path = os.path.join(directory, filename)
            data = pd.DataFrame()
            if 'stmt' in filename:
                try:
                    # Read all lines from the file into a list
                    with open(filename, 'r') as file:
                        lines = file.readlines()
                
                    # Skip the first 6 lines (summary lines)
                    lines = lines[6:]
                    csv_content = ''.join(lines)
                    # Read the file, skipping lines with parsing errors
                    data = pd.read_csv(StringIO(csv_content))
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
                    continue
            else:   
                data = pd.read_csv(file_path, index_col = False)
            #Process each file based on its filename
            data = process_file(data, filename)
            #Comebine the data 
            combined_data = pd.concat([combined_data, data], ignore_index = True)
            print('done processing for ' +filename + '\n')

    # Save the combined data to a new CSV file
    combined_data = combined_data.drop(columns=['Post Date','Memo', 'Running Bal.'])
    desired_order = ['Date', 'Description', 'Category', 'Type', 'Amount']
    combined_data = combined_data[desired_order]
    combined_data.to_csv(os.path.join(directory, 'results.csv'), index=False)
    print("Saving combined data")
if __name__ == "__main__":
    directory = input("Enter the directory path: ")
    print(directory)
    main(directory)