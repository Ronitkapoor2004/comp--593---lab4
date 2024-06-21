import sys 
import os
import re
import pandas as pd

def main():
    log_file = get_log_file_path_from_cmd_line()
    dict = tally_port_traffic(log_file)
    for port_no in dict:
        if dict[port_no] == 100 or dict[port_no] > 100:
            generate_port_traffic_report(log_file, port_no)
    generate_invalid_user_report(log_file)
    generate_source_ip_log(log_file, '220.195.35.40')

# TODO: Step 3
def get_log_file_path_from_cmd_line():
    if len(sys.argv) < 2:
        print("Error: The file path of gateway log is not provided!")
    else:
        if os.path.exists(sys.argv[1]) == False:
            print("Error: File does not exists!")
    return sys.argv[1]

# TODO: Steps 4-7
def filter_log_by_regex(log_file, regex, ignore_case=True, print_summary=False, print_records=False):
    """Gets a list of records in a log file that match a specified regex.

    Args:
        log_file (str): Path of the log file
        regex (str): Regex filter
        ignore_case (bool, optional): Enable case insensitive regex matching. Defaults to True.
        print_summary (bool, optional): Enable printing summary of results. Defaults to False.
        print_records (bool, optional): Enable printing all records that match the regex. Defaults to False.

    Returns:
        (list, list): List of records that match regex, List of tuples of captured data
    """
    L = list()
    L1 = list()
    with open(log_file,'r') as file:
        for line in file:
            if ignore_case == True:
                match = re.search(regex, line, re.IGNORECASE)
                if match:
                    L.append(line[:-1])
                    matched_str = (match.groups())
                    L1.append(matched_str)
            else:
                match = re.search(regex, line, re.IGNORECASE)
                if match:
                    record = [line]
                    L.append(record[:-1])
                    matched_str = (match.group())
                    L1.append(matched_str)
    if print_records == True:
        for record in L:
            print(L)
    if print_summary == True:
        if ignore_case == True:
            print(f"The number of records match in the log file are {len(L)} and case-insensitive regex matching is performed.")
        else:
            print(f"The number of records match in the log file are {len(L)} and case-sensitive regex matching is performed.")
    return (L,L1)

# TODO: Step 8
def tally_port_traffic(log_file):
    regex = 'DPT=(.*?) '
    captured_data_list = filter_log_by_regex(log_file, regex)[1]
    dict = {}
    L = []
    for i in captured_data_list:
        L.append(i[0])
    for key in L:
        c_value = L.count(key)
        dict[key] = c_value        
    return dict

# TODO: Step 9
def generate_port_traffic_report(log_file, port_number):
    file_path = os.path.abspath(__file__)
    dir_name = os.path.dirname(file_path)
    DPT_file_name = f'destination_port_{port_number}_report.csv'
    DPT_path = os.path.join(dir_name, DPT_file_name)

    regex = f'(.*?\d) (.*?) .*?SRC=(.*?) DST=(.*?) .*?SPT=(.*?) DPT={port_number} '
    captured_data = filter_log_by_regex(log_file, regex)[1]
    
    dict={}

    Date=[]
    Time=[]
    SRCip=[]
    DSTip=[]
    SPTno=[]
    DPTno=[]

    for data in captured_data:
        Date.append(data[0])
        Time.append(data[1])
        SRCip.append(data[2])
        DSTip.append(data[3])
        SPTno.append(data[4])
        DPTno.append(port_number)

    dict['Date']=Date
    dict['Time']=Time
    dict['Source IP address']=SRCip
    dict['Destination IP address']=DSTip
    dict['Source port no']=SPTno
    dict['Destination port no']=DPTno

    df = pd.DataFrame(dict)
    with open( DPT_path, 'a') as file:
        df.to_csv(DPT_path, index=False)

    return

# TODO: Step 11
def generate_invalid_user_report(log_file):
    file_path = os.path.abspath(__file__)
    dir_name = os.path.dirname(file_path)
    filenm = 'invalid_users.csv'
    filepath = os.path.join(dir_name, filenm)

    regex = '(.*?\d) (\d+:\d+:\d+).*? user (.*?) from (\d+.\d+.\d+.\d+)'
    captured_data=filter_log_by_regex(log_file, regex)[1]

    dict={}

    Date=[]
    Time=[]
    user=[]
    ip_address=[]

    for data in captured_data:
        Date.append(data[0])
        Time.append(data[1])
        user.append(data[2])
        ip_address.append(data[3])

    dict['Date']=Date
    dict['Time']=Time
    dict['Username']=user
    dict['IP Address']=ip_address

    df = pd.DataFrame(dict)
    with open( filepath, 'a') as file:
        df.to_csv(filepath, index=False)
    return

# TODO: Step 12
def generate_source_ip_log(log_file, ip_address):
    file_path = os.path.abspath(__file__)
    dir_name = os.path.dirname(file_path)

    new_ip_address = re.sub('\.','_',ip_address)

    filenm = f'source_ip_{new_ip_address}.log'
    filepath = os.path.join(dir_name, filenm)

    regex=f'.*?SRC=({ip_address}) '

    captured_data=filter_log_by_regex(log_file, regex)[0]

    with open(filepath,'a') as file:
        for data in captured_data:
            newline_in_data = data + '\n'
            file.write( newline_in_data)

    return

if __name__ == '__main__':
    main()