# Boolean Retrieval Model
This project implements a basic information retrieval system capable of processing boolean and proximity queries. The system utilizes inverted and positional indexes to efficiently retrieve relevant document IDs based on user queries.

## Features
* Supports boolean queries including AND, OR, and NOT operations.
* Implements proximity queries to find terms within a specified distance of each other.
* Utilizes inverted and positional indexes for efficient query processing.
* Provides a simple GUI interface for user interaction.

## Getting Started
To run the information retrieval system, follow these steps:

* Ensure you have Python 3.12 installed.
* Install NLTK, tkinter and customtkinter library using pip install NLTK etc.
* Make sure Stopword-List.txt and the Research Paper directory containing all the documents is in your current working directory.
* Run the files in an IDE.
* Run this command to download the tokennizer nltk.download('punkt')
* Run the index_creation.py script first using python index_creation.py to create and save the indexes.
* Then run the query_processing.py using python query_processing.py for queries.
* Use the tkinter GUI interface to input queries and press 'Process Query' button to retrieve the required document IDs.
* Press the 'Exit' button to exit the program.

## Usage
 ### Boolean Queries
 Boolean queries can be constructed using AND, OR, and NOT operations. Simply enter your query in the provided text box and click the "Process Query" button to retrieve relevant documents.

 ### Proximity Queries
 Proximity queries allow users to find terms within a specified distance of each other. Enter your query in the format 'term1 term2 /distance' and click "Process Query" to retrieve relevant documents.

## License
 This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
* This project was inspired by information retrieval concepts and algorithms.
* Special thanks to the developers of NLTK for providing essential natural language processing tools.
