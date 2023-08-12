import streamlit as st
import nltk
from nltk import pos_tag, ne_chunk
from nltk.tokenize import word_tokenize, sent_tokenize
from textblob import TextBlob
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

nltk.download('punkt')
nltk.download('maxent_ne_chunker')
nltk.download('words')

def sumy_summarizer(docx):
    parser = PlaintextParser.from_string(docx, Tokenizer("english"))
    lex_summarizer = LexRankSummarizer()
    summary = lex_summarizer(parser.document, 3)
    summary_list = [str(sentence) for sentence in summary]
    result = ' '.join(summary_list)
    return result

# Function to Analyze Tokens and Lemma using NLTK
@st.cache
def text_analyzer(my_text):
    tokens = word_tokenize(my_text)
    lemma = [token for token in tokens]  # NLTK doesn't have built-in lemmatization like spaCy
    allData = [{"Token": token, "Lemma": lemma} for token, lemma in zip(tokens, lemma)]
    return allData

# Function For Extracting Named Entities using NLTK
@st.cache
def entity_analyzer(my_text):
    sentences = sent_tokenize(my_text)
    entities = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        tagged = pos_tag(words)
        entities.extend(ne_chunk(tagged))
    named_entities = [(str(entity), entity.label()) for entity in entities if isinstance(entity, nltk.Tree)]
    allData = [{"Token": entity[0], "Entity": entity[1]} for entity in named_entities]
    return allData

def main():
    st.title("NLPiffy with Streamlit")
    st.subheader("Natural Language Processing On the Go..")
    st.markdown("""
        #### Description
        + This is a Natural Language Processing (NLP) Based App useful for basic NLP tasks:
        Tokenization, NER, Sentiment Analysis, Summarization
        """)

    st.sidebar.header("Choose Input Method")
    input_method = st.sidebar.radio("Select Input Method", ["Upload a .txt file", "Type Text"])

    uploaded_file = None  # Placeholder for uploaded file

    if input_method == "Upload a .txt file":
        uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
        if uploaded_file is not None:
            file_contents = uploaded_file.read().decode("utf-8")
            st.text_area("Uploaded Text", file_contents, key="uploaded_text")

    elif input_method == "Type Text":
        user_text = st.text_area("Enter Text", "Type Here ..", key="user_text")

    if uploaded_file is not None or input_method == "Type Text":
        if st.checkbox("Show Tokens and Lemma"):
            st.subheader("Tokenize Your Text")
            if st.button("Analyze Tokenization"):
                nlp_result = text_analyzer(file_contents if uploaded_file is not None else user_text)
                st.json(nlp_result)

        if st.checkbox("Show Named Entities"):
            st.subheader("Analyze Named Entities")
            if st.button("Extract Entities"):
                entity_result = entity_analyzer(file_contents if uploaded_file is not None else user_text)
                st.json(entity_result)

        if st.checkbox("Show Sentiment Analysis"):
            st.subheader("Analyze Sentiment")
            if st.button("Analyze Sentiment"):
                blob = TextBlob(file_contents if uploaded_file is not None else user_text)
                result_sentiment = blob.sentiment
                st.success(result_sentiment)

        if st.checkbox("Show Text Summarization"):
            st.subheader("Summarize Text")
            if st.button("Summarize"):
                st.text("Using Sumy Summarizer ..")
                summary_result = sumy_summarizer(file_contents if uploaded_file is not None else user_text)
                st.success(summary_result)

if __name__ == '__main__':
    main()
