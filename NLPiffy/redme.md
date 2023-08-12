NLPiffy: Natural Language Processing App with Streamlit
NLPiffy is a Natural Language Processing (NLP) based web application built using Streamlit. This app provides basic NLP functionalities such as Tokenization, Named Entity Recognition (NER), Sentiment Analysis, Part-of-Speech (POS) Tagging, Dependency Parsing, and Text Summarization.

Features
Tokenization: Analyze and display the tokens and lemmas of the input text.
Named Entity Recognition (NER): Extract and visualize named entities from the input text.
Sentiment Analysis: Determine the sentiment (polarity and subjectivity) of the input text.
Part-of-Speech (POS) Tagging: Identify and display the parts of speech of each token.
Dependency Parsing: Visualize the syntactic dependencies between words in the input text.
Text Summarization: Summarize the input text using LexRank algorithm.
Getting Started
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/nlpiffy.git
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Run the Streamlit app:

bash
Copy code
streamlit run nlp_project.py
Open your web browser and go to http://localhost:8501.

Usage
Choose NLP Method: Select between spaCy and NLTK for NLP processing.
Choose Input Method: Upload a .txt file or enter text manually.
Select NLP Task: Check the tasks you want to perform on the input text.
Analyze: Click the buttons to perform the selected NLP tasks.
Technologies Used
Streamlit: Interactive web application framework.
spaCy: NLP library for advanced natural language processing.
NLTK: Natural Language Toolkit for various NLP tasks.
TextBlob: Library for processing textual data.
Credits
This project was inspired by various NLP tutorials and resources available online. Special thanks to the Streamlit, spaCy, and NLTK communities for their valuable contributions.


