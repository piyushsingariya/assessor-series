
# use this command to download more than 1000 usernmes: wget http://www2.census.gov/topics/genealogy/2000surnames/Top1000.xls

#!/usr/bin/env python
'''
Author: Piyush Singariya
Inspired From: Christopher S. Duffy
Date: June 2019
Name: assessor_mark7.py
Purpose: To generate a username list from the US Census Top 1000 surnames and other lists'''


import sys, string
import arparse, os
from collections import namedtuple
try:
    import xlrd
except:
    sys.exit("[!] Please install the xlrd library: pip install xlrd")

def unique_list(list_sort, verbose):
    noted = []
    if verbose >0:
        print("[*] removing duplicates while maintaining order")
        [noted.append(item) for item in list_sort if not noted.count(item)] # List comprehension
        return noted  

# using a form of a tuple called a named tuple to accept each row of the spreadsheet
def census_parser(filename, verbose):
    # creating the named tuple
    CensusTuple = namedtuple("Census", 'name, rank, count, prop100k, cum_prop100k, pctwhite, pctblack, pctapi, pctaian, pct2prace, pcthispanic')

    # variables to hold the workbook, spreadsheet by the name, and the total rows and the initial row of the spreadsheet.
    
    worksheet_name = 'top1000'
    # Define work book and work sheet variables
    workbook = xlrd.open_workbook(filename)
    spreadsheet = workbook.sheet_by_name(worksheet_name)
    total_rows = spreadsheet.nrows - 1
    current_row = -1

    # initial variable to hold the resulting value and the actual alphabet.
    
    # Define holder for details
    username_dict = {}
    surname_dict = {}
    alphabet = list(string.ascii_lowercase)

    while current_row<total_rows:
        row = spreadsheet.row(current_row)
        current_row +=1
        entry = CensusTuple(*tuple(row)) # Passing the value of the row as a tuple into the namedtuple
        surname_dict[entry.rank] = entry
        cellname = entry.name
        cellrank = entry.rank
        for letter in alphabet:
            if "." not in str(cellrank.value):
                if verbose >1:
                    print("[-] Eliminating table headers")
                break
            username = letter + str(cellname.value.lower())
            rank = str(cellrank.value)
            username_dict[username] = rank
    username_list =  sorted(username_dict, key=lambda key:username_dict[key])
    return(surname_dict, username_dict, username_list)

def username_file_parser(prepend_file, append_file, verbose):
    if prepend_file:
        put_where = "begin"
        filename = prepend_file
    elif append_file:
        put_where = "end"
        filename = append_file
    else:
        sys.exit("[!] There was an error in processing the supplemental username list!")
        with open(filename) as file:
            lines = [line.rstrip('\n') for line in file]
    if verbose>1:
        if 'end' in put_where:
            print("[*] Appending %d entries to the username list") % (len(lines)) 
        else:
            print("[*] Prepending %d entries to the username list") % (len(lines))
    return(lines, put_where)

def combine_usernames(supplemental_list, put_where, username_list, vevrbose):
    if 'begin' in put_where:
        username_list[:0] = supplemental_list # Prepend with a slice
    if 'end' in put_where:
        username_list.extend(supplemental_list)
        username_list = unique_list(username_list, vevrbose)
        return (username_list)
        
# This last function in this script writes the details to a file.

def write_username_file(username_list, filename, domain, verbose):
    open(filename, 'w').close() # Deletes the content of the filename
    
    if domain:
        domain_filename = filename + "_" + domain
        email_list = []
        open(domain_filename, 'w').close()
    if verbose >1:
        print("[*] Writing to %s") % (filename)
    with open(filename, 'w') as file:
        file.write('\n'.join(username_list))
    if domain:
        if verbose:
            print("[*] Writing domain supported list to %s") % (domain_filename)
        for line in username_list:
            email_address = line + "@" +domain
            email_list.append(email_address)
        with open(domain_filename, 'w') as file:
            file.write('\n'.join(email_list))
    return

if __name__ == '__main__':
    # If script is execcuted at the CLI
    usage = '''usage: %(prog)s [-c census.xlsx] [-f output_filename] [-p prepend_filename] [-d domain_name] -q -v -vv -vvv'''
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument("-c", "--census", type=str, help="The census file that will be used to create usernames, this can be retrieved like so:\n wget http://www2.census.gov/topics/genealogy/2000surnames/Top1000.xls", action="store", dest="census_file")
    parser.add_argument("-f", "--filename", type=str, help="Filename for output the usernames", action="store", dest="filename")
    parser.add_argument("-a","--append", type=str, action="store", help="A username list to append to the list generated from the census", dest="append_file")
    parser.add_argument("-p","--prepend", type=str, action="store", help="A username list to prepend to the list generated from the census", dest="prepend_file")
    parser.add_argument("-d","--domain", type=str, action="store", help="The domain to append to usernames", dest="domain_name")
    parser.add_argument("-v", action="count", dest="verbose", default=1, help="Verbosity level, defaults to one, this outputs each command and result")
    parser.add_argument("-q", action="store_const", dest="verbose", const=0, help="Sets the results to be quiet")
    parser.add_argument('--version', action='version', version='%(prog)s 0.42b')
    args = parser.parse_args()

    # Set Constructors
    census_file = args.census_file # Census
    filename = args.filename # Filename for outputs
    verbose = args.verbose # Verbosity Level
    append_file = args.append_file # Filename for appending usernames to the output
    prepend_file = args.prepend_file # Filename to prepend to the usernames to the output file
    domain_name = args.domain_name  # The name of the domain to be appended to the username lists
    dir = os.getcwd() # Get current working directory

    # Argument Validator
    if len(sys.argv) ==1:
        parser.print_help()
        sys.exit(1)
    if append_file and prepend_file:
        sys.exit("[!] Please select either prepend or append for a file not both")
    
    if not filename:
        if os.name !=  'nt':
            filename =dir +"/census_username_list"
        else:
            filename = dir + '\\census_username_list'
    else:
        if filename:
            if '\\' or '/' in filename:
                if verbose > 1:
                    print("[*] Using filename: %s") % (filename)
            else:
                if os.name != "nt":
                    filename = dir + "/" + filename
                else:
                    filename = dir +"\\" + filename
                    if verbose > 1:
                        print("[*] Using filename: %s") % (filename)

# define working variables
sur_dict = {}
user_dict = {}
user_list = {}
sup_username = []
target = []
combine_users = []

# Process census file
if not census_file:
    sys.exit("[!] You did not provide a census file!")
else:
    sur_dict, user_dict, user_list = census_parser(census_file, verbose)

# Process supllemental username file
if append_file or prepend_file:
    sup_username, target = username_file_parser(prepend_file, append_file, verbose)
    combined_users = combine_usernames(sup_username, target, user_list, verbose)
else:
    combine_users = user_list

write_username_file(combine_usernames, filename, domain_name, verbose)