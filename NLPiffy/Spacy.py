import streamlit as st
import spacy
from textblob import TextBlob
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

def sumy_summarizer(docx):
    parser = PlaintextParser.from_string(docx, Tokenizer("english"))
    lex_summarizer = LexRankSummarizer()
    summary = lex_summarizer(parser.document, 3)
    summary_list = [str(sentence) for sentence in summary]
    result = ' '.join(summary_list)
    return result



@st.cache
def pos_tagger(docx):
    nlp = spacy.load('en_core_web_sm')
    docx = nlp(docx)
    pos_tags = [f'{token.text}: {token.pos_}' for token in docx]
    return pos_tags

@st.cache
def dependency_parser(docx):
    nlp = spacy.load('en_core_web_sm')
    docx = nlp(docx)
    dependencies = [f'{token.text} --{token.dep_}--> {token.head.text}' for token in docx]
    return dependencies


@st.cache
def text_analyzer(docx):
    nlp = spacy.load('en_core_web_sm')
    docx = nlp(docx)
    allData = [('"Token":{},\n"Lemma":{}'.format(token.text, token.lemma_)) for token in docx]
    return allData

@st.cache
def entity_analyzer(docx):
    nlp = spacy.load('en_core_web_sm')
    docx = nlp(docx)
    tokens = [token.text for token in docx]
    entities = [(entity.text, entity.label_) for entity in docx.ents]
    allData = ['"Token":{},\n"Entities":{}'.format(tokens, entities)]
    return allData


def main():
    st.title("NLPiffy with Streamlit")
    st.subheader("Natural Language Processing On the Go..")
    st.markdown("""
        #### Description
        + This is a Natural Language Processing (NLP) Based App useful for basic NLP tasks:
        Tokenization, NER, Sentiment Analysis, POS Tagging, Dependency Parsing, Summarization
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

    if input_method == "Upload a .txt file" or input_method == "Type Text":
        if st.checkbox("Show Tokens and Lemma"):
            st.subheader("Tokenize Your Text")
            if st.button("Analyze Tokenization"):
                nlp_result = text_analyzer(file_contents if uploaded_file is not None else user_text)
                st.json(nlp_result)

        if st.checkbox("Show Part-of-Speech Tagging"):
            st.subheader("Perform Part-of-Speech Tagging")
            if st.button("Tag POS"):
                pos_result = pos_tagger(file_contents if uploaded_file is not None else user_text)
                st.json(pos_result)

        if st.checkbox("Show Dependency Parsing"):
            st.subheader("Perform Dependency Parsing")
            if st.button("Parse Dependencies"):
                dep_result = dependency_parser(file_contents if uploaded_file is not None else user_text)
                st.json(dep_result)

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





