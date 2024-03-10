import os
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

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

def create_positional_index(total_tokens):
    """
    This function creates a positional index from the given tokens.

    Args:
        total_tokens (list): A list of processed tokens from which the positional index is to be created.

    Returns:
        terms (dict): A dictionary representing the positional index.
    """

    terms = {} # declare an empty dictionary for the positional index
    porter_stemmer = PorterStemmer() # initialize the stemmer

    # get the stopwords. Although stopwords is not going to be inserted in the positional index, we still need them to find the correct positions of the rest of the words
    stopwords = get_stopwords()
    doc = get_docIDs() # get the docIDs

    for i, tokens in enumerate(total_tokens): # loop through each token in total_tokens, and then loop through each word in the token
        for j, word in enumerate(tokens):
            if word not in stopwords: # filter the stopwords
                word = porter_stemmer.stem(word) # Stem the word
                if word[-1] == "'": # if the word ends with an apostrophe, remove it
                    word = word.rstrip("'")
                if word in terms: # if the word is already in the positional index, add the docID to the index
                    if doc[i] in terms[word]: # if the docID is already in the index for that word, add the position
                        terms[word][doc[i]].append(j)
                    else: # else add the docID as well as the position
                        terms[word][doc[i]] = [j]
                else: # add the word in the index along with the docID and the position
                    terms[word] = {doc[i]: [j]}
    return terms

def create_inverted_index(total_tokens):
    """
    This function creates an inverted index from the given tokens.

    Args:
        total_tokens (list): A list of tokens from which the inverted index is to be created.

    Returns:
        terms (dict): A dictionary representing the inverted index.
    """

    terms = {} # an empty dictionary for the inverted index
    porter_stemmer = PorterStemmer() # initialize the stemmer
    stopwords = get_stopwords() # get the stopwords
    doc = get_docIDs() # get the docIDs

    for i, tokens in enumerate(total_tokens): # loop through each token in total_tokens and remove the stopwords
        total_tokens[i] = [c for c in tokens if c not in stopwords]

    for i, tokens in enumerate(total_tokens): # loop through each token in total_tokens again
        for word in tokens: # loop through each word in tokens
            word = porter_stemmer.stem(word) # stem the word
            if word[-1] == "'": # remove the apostrophe
                word = word.rstrip("'")
            if word in terms: # if the word is already in the inverted index
                if doc[i] not in terms[word]: # append the docID if it isn't in the index
                    terms[word].append(doc[i])
            else: # add the word along with the docID
                terms[word] = [doc[i]]
    return terms    

def preprocessing():
    """
    This function is used to preprocess the text files in the 'ResearchPapers' directory.

    It reads each file, tokenizes the text, removes punctuation and converts the text to lowercase. 
    It also splits the tokens at '.' and '-'. Assumes the 'ResearchPapers' folder is in your current working directory.

    Returns:
        total_tokens (list): A list of preprocessed tokens from all the files.
    """

    total_tokens = [] # an empty list to store the tokens from all the files
    doc = get_docIDs() # get the docIDs

    for i in doc: # iterate through each doc
        tokens = []
        with open('ResearchPapers/' + str(i) +'.txt', 'r') as f: # open the file corresponding to the current document ID
            while True:
                text = f.readline() # read a line from the file
                if not text: # if the line is empty (which means end of file), break the loop
                    break
                tokens += word_tokenize(text) # tokenize the line and add the tokens to the list

        j = 0
        while j < len(tokens): # loop through each token
            # remove symbols and numbers from the start and end of the token and convert it to lowercase (case folding)
            tokens[j] = tokens[j].lstrip('0123456789!@#$%^&*()-_=+[{]}\|;:\'",<.>/?`~').rstrip('0123456789!@#$%^&*()-_=+[{]}\|;:\'",<.>/?`~').lower()
            if '.' in tokens[j]: # if '.' exists in a word, split the word at that point and add the splitted words at the end of the tokens list while removing the original word
                word = tokens[j].split('.')
                del tokens[j]
                tokens.extend(word)
            elif '-' in tokens[j]: # do the same for words with '-'
                word = tokens[j].split('-')
                del tokens[j]
                tokens.extend(word)
            j += 1 # move the index forward
        tokens = [c for c in tokens if c.isalpha()] # filter out any strings that contain symbols, numbers, etc.
        total_tokens.append(tokens) # add the processed tokens as a seperate list. Did this to keep track of which tokens appear in which docs (needed to construct indexes). List at index 0 indicate tokens found in doc 1 and so on.
    return total_tokens

def save_indexes():
    """
    This function preprocesses the data to generate tokens, creates an inverted index and a positional index from these tokens, and then saves these indexes to 'inverted_index.txt' and 'positional_index.txt' respectively.

    The preprocessing function is expected to return a list of tokens.
    The create_inverted_index function takes the tokens as input and returns a dictionary where the keys are the unique tokens and the values are the documents in which they appear.
    The create_positional_index function also takes the tokens as input and returns a dictionary where the keys are the unique tokens and the values are the positions in which they appear in the document.

    The output files 'inverted_index.txt' and 'positional_index.txt' contain the string representation of the respective dictionaries, with each key-value pair on a new line.
    """

    tokens = preprocessing() # preprocessing function is called
    inverted_index = create_inverted_index(tokens) # create_inverted_index function is called
    positional_index = create_positional_index(tokens) # create_positional_index function is called

    with open('inverted_index.txt', 'w') as f: # the inverted index is written to 'inverted_index.txt'
        for key, value in inverted_index.items(): # loop through each key-value pair in the inverted index and output it to the file
            f.write('{}:'.format(key))
            for i in value:
                f.write('{} '.format(i))
            f.write('\n')
    with open('positional_index.txt', 'w') as f: # do the same for positional index
        for key, value in positional_index.items():
            for k, v in value.items():
                f.write('{}:{}.'.format(key, k))
                for i in v:
                    f.write('{} '.format(i))
                f.write('\n')

def main():
    if (not os.path.isfile('inverted_index.txt') and not os.path.isfile('positional_index,txt')): # check if the indexes already exist, if they don't, call the save_indexes function
        save_indexes()
    else:
        print("Indexes already exist")

if __name__ == '__main__':
    main() # execute the main function