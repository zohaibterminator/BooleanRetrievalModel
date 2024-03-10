import os
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import customtkinter as ctk
import tkinter as tk

def extract_indexes():
    """
    This function is used to extract the inverted index and the positional index from their respective text files.

    Returns:
        inverted_index (dict): The extracted inverted index.
        positional_index (dict): The extracted positional index.
    """

    inverted_index = {}
    positional_index = {}
    with open('inverted_index.txt', 'r') as f:
        while True:
            element = f.readline() # read a line from the file
            if element == '': # if the line is empty (which means end of file), break the loop
                break
            term, posting = element.split(':') # split the line at ':'. the first part of the split line is the term, and the second is the postings list
            posting = posting.split() # split the positions at whitespace
            posting = [int(c) for c in posting if c != '' and c != '\n'] # convert the positions to a list of integers and remove any empty strings or newline characters
            inverted_index[term] = posting # add the term and its posting list to the inverted index

    with open('positional_index.txt', 'r') as f: # do the same for the positional index
        while True:
            element = f.readline()
            if element == '':
                break
            element = element.split(':')
            term = element[0]
            docID, positions = element[1].split('.')
            positions = positions.split()
            positions = [int(c) for c in positions if c != '' and c != '\n']
            if term in positional_index: # if the term is already in the positional index, append the positions to the term's dictionary. Otherwise append both docID and the positions
                positional_index[term][int(docID)] = positions
            else:
                positional_index[term] = {int(docID): positions}
    return inverted_index, positional_index

def get_docIDs():
    """
    This function is used to extract document IDs based on the names of the files in the 'ResearchPapers' directory.

    It gets the current working directory and lists all the files in the 'ResearchPapers' directory. 
    It then extracts the document IDs from the names of these files, sorts them, and returns the sorted list.
    Assumes the 'ResearchPapers' folder is in your current working directory.

    Returns:
        docID (list): A sorted list of document IDs extracted from the file names in the 'ResearchPapers' directory.
    """

    curr_dir = os.getcwd() # get the current directory
    docID = [int(c.rstrip('.txt')) for c in os.listdir(curr_dir + '\ResearchPapers')] # extract the docIDs from the names of the files in the ResearchPapers directory
    docID.sort()
    return docID

def get_stopwords():
    """
    This function is used to extract stopwords from 'Stopword-List.txt' file.

    It reads each line from the file, and if the line is not empty, it appends the line to the stopwords list.
    The function continues this process until it reaches the end of the file. Assumes the file is in your current working directory.

    Returns:
        stopwords (list): A list of stopwords extracted from the file.
    """

    stopwords = []
    with open('Stopword-List.txt', 'r') as f: # the 'Stopword-List.txt' file is opened in read mode
        while True:
            text = f.readline() # each line from the file is read one by one
            if not text: # if the line read is empty (which means end of file), the loop is broken
                break
            stopwords.append(text) # else append the read line to the stopwords list

    stopwords = [c.rstrip(' \n') for c in stopwords if c != '\n'] # a new list is created from stopwords, excluding any newline characters. Newline characters are also removed from the strings.
    return stopwords

def INTERSECTION(p1, p2):
    """
    This function returns the intersection of two lists.

    Args:
        p1 (list): The first list.
        p2 (list): The second list.

    Returns:
        result (list): A list containing the elements common to p1 and p2.
    """

    result = [c for c in p1 if c in p2] # a new list is created from p1, containing only the elements that are also in p2
    return result

def UNION(p1, p2):
    """
    This function returns the union of two lists.

    Args:
        p1 (list): The first list.
        p2 (list): The second list.

    Returns:
        result (list): A list containing the elements from both p1 and p2, without duplicates.
    """

    # add the elements of p1 and p2 to a new list
    result = p1
    result.extend(p2)
    result = list(set(result)) # convert the list to a set to remove duplicates, and then convert the set back to a list
    return result

def NOT(p1):
    """
    This function returns the elements that are in a predefined list but not in the input list.

    Args:
        p1 (list): The input list.

    Returns:
        result (list): A list containing the elements that are in 'doc' but not in p1.
    """

    doc = get_docIDs() # get the docIDs
    result = [c for c in doc if c not in p1] # use list comprehension to create a new list that contains only the elements that are in doc but not in p1
    return result

def BoolQueryProcessing(query):
    """
    This function processes the query and returns the result based on the type of query.

    Args:
        query (str): The query to be processed.

    Returns:
        result (list): The result of the query.
    """

    query = query.split() # split the query into words
    porter_stemmer = PorterStemmer() # initialize the stemmer
    stopwords = get_stopwords() # get the stopwords
    inverted_index, positional_index = extract_indexes() # extract the inverted index and positional index

    for i, word in enumerate(query): # loop through each word in the query
        if word in ['AND', 'OR', 'NOT']: # if the word is a boolean operator, skip it
            continue
        temp = porter_stemmer.stem(word) # stem the word
        if temp[-1] == "'": # remove the apostrophe
            temp = word.rstrip("'")
        else:
            query[i] = temp

    if 'AND' in query: # if the query contains 'AND', 'OR' or 'NOT, split the query at that point and process the two parts separately
        index = query.index('AND')
        t1 = query[:index] # splitting the query into two parts
        t2 = query[index+1:]
        p1 = BoolQueryProcessing(' '.join(t1)) # combine the query into a string and recursively call the function to process the first part
        p1 = p1.split() # split the result into a list
        p1 = [int(c) for c in p1]
        p2 = BoolQueryProcessing(' '.join(t2)) # combine the query into a string and recursively call the function to process the first part
        p2 = p2.split()
        p2 = [int(c) for c in p2]
        result = INTERSECTION(p1, p2) # find the intersection of the results
    elif 'OR' in query:
        index = query.index('OR')
        t1 = query[:index]
        t2 = query[index+1:]
        p1 = BoolQueryProcessing(' '.join(t1))
        p1 = p1.split()
        p1 = [int(c) for c in p1]
        p2 = BoolQueryProcessing(' '.join(t2))
        p2 = p2.split()
        p2 = [int(c) for c in p2]
        result = UNION(p1, p2) # find the union of the results
    elif 'NOT' in query:
        index = query.index('NOT')
        t1 = query[index+1:]
        p1 = BoolQueryProcessing(' '.join(t1))
        p1 = p1.split()
        p1 = [int(c) for c in p1]
        result = NOT(p1)
    else: # if the query contains only a single term
        term = query[0] # extract the term
        result = inverted_index.get(term, []) # get the postings list for the term from the inverted index. Will get an empty list if the term is not found

    result = ''.join([str(c) + ' ' for c in result]) # convert the result to a string
    return result

def ProxQueryProcessing(query):
    """
    This function processes a proximity query.

    Parameters:
    query (str): The proximity query to be processed.

    Returns:
    str: A string of document IDs that satisfy the proximity query.
    """

    query = query.split() # split the query into words
    porter_stemmer = PorterStemmer() # initialize the stemmer
    stopwords = get_stopwords() # get the stopwords
    inverted_index, positional_index = extract_indexes() # extract the inverted and positional indexes

    position = query.pop(-1)
    position = int(position[-1])

    if query[0] not in stopwords: # if the word is not a stopword, stem it
        word = porter_stemmer.stem(query[0].lower()) # stem the first word in the query
        if word[-1] == "'": # remove the apostrophe
                word = word.rstrip("'")
        query[0] = word
    
    if query[1] not in stopwords: # if the word is not a stopword, stem it
        word = porter_stemmer.stem(query[1].lower()) # stem the second word in the query
        if word[-1] == "'": # remove the apostrophe
            word = word.rstrip("'")
        query[1] = word

    docs = [] # create a list to store the postings list for each term in the query
    if query[0] not in stopwords:
        docs.append(inverted_index[query[0]]) # get the postings list for the first term
    else:
        docs.append([])
    
    if query[1] not in stopwords:
        docs.append(inverted_index[query[1]]) # get the postings list for the second term
    else:
        docs.append([])

    common_docs = INTERSECTION(docs[0], docs[1]) # find the common documents in the postings list of the two terms

    result = [] # create a list to store the result
    for i in common_docs: # loop through the common documents
        pp1 = positional_index[query[0]][i] # get the positions of the first term in the document
        pp2 = positional_index[query[1]][i] # get the positions of the second term in the document

        # now we need to find the positions of the second term that are within the specified proximity of the positions of the first term
        j = 0
        k = 0
        while j != len(pp1):
            while k != len(pp2):
                if abs(pp1[j] - pp2[k]) <= position: # if the positions of the two terms are within the specified proximity, add the document to the result
                    if i not in result: # if the document is not already in the result, add it
                        result.append(i)
                elif pp2[k] > pp1[j]: # if the position of the second term is greater than the position of the first term, break the loop
                    break 
                k+=1
            j+=1

    result = ''.join([str(c) + ' ' for c in result]) # convert the result to a string
    return result

def process_query():
    """
    This function retrieves a user's query from a GUI text entry field, processes the query, and displays the result in a GUI label.

    The function assumes that the query is a proximity query if it contains a '/' character, and a boolean query otherwise.
    """

    query = entry.get() # get the query from the text entry field

    if '/' in query: # if the query contains a '/', it is a proximity query, so call the ProxQueryProcessing function
        result = ProxQueryProcessing(query)
    else:  # otherwise, it is a boolean query, so call the BoolQueryProcessing function
        result = BoolQueryProcessing(query)

    if result == '': # if the result is empty, display a message
        result = 'No documents found'
    output_label.configure(state='normal') # enable the output label
    output_label.delete(0, tk.END) # clear the output label
    output_label.insert(0, result) # insert the result into the output label
    output_label.configure(state=tk.DISABLED) # again disable the output label

ctk.set_appearance_mode('Dark') # set the appearance mode to dark
ctk.set_default_color_theme('dark-blue') # set the default color theme

root = ctk.CTk() # create a new window
root.geometry('500x400') # set the window size

root.title('Boolean Query Model') # set the window title
label1 = ctk.CTkLabel(root, text="Boolean Query Model", font=("Verdana", 20), fg_color="transparent") # create a label "Boolean Query Model" with a font size of 20 and transparent foreground color
label1.place(relx=0.5, rely=0.2, anchor=tk.CENTER) # place the label according to the given co-ordinated relative to x and y axis
label2 = ctk.CTkLabel(root, text="Enter Query", fg_color="transparent") # create another label "Enter Query" with a transparent foreground color
label2.place(relx=0.5, rely=0.3, anchor=tk.CENTER) # place the at the center of the window
entry = ctk.CTkEntry(root, width=200, bg_color='black') # create a text entry field with a width of 200 and a black background color
entry.place(relx=0.5, rely=0.4, anchor=tk.CENTER) # place the text entry field in the window
process_button = ctk.CTkButton(root, text="Process Query", font=("Helvetica", 12), bg_color='white', fg_color="#B6C8A9", hover_color="white", text_color = "black", command=process_query) # create a button "Process Query" with a font size of 12 and white background color and black text color. The button calls the process_query function when clicked
process_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER) # place the button in the window
exit_button = ctk.CTkButton(root, text="Exit", font=("Helvetica", 12), bg_color='white', fg_color="#B6C8A9", hover_color="white", text_color = "black", command=root.destroy) # create a button "Exit" with a font size of 12 with white background color and black text color. The button terminates the window when clicked
exit_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER) # place the button in the window
output_label = ctk.CTkEntry(root, width=400, height=50, bg_color='black') # create a text entry field with a width of 400, a height of 50, and a black background color
output_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER) # place the text entry field in the window
output_label.configure(state='readonly') # set the state of the text entry field to readonly (disable it)


if __name__ == "__main__":
    root.mainloop() # run the window