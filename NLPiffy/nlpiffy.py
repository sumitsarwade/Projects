import streamlit as st
import spacy
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

def nltk_pos_tagger(my_text):
    tokens = word_tokenize(my_text)
    pos_tags = pos_tag(tokens)
    return pos_tags

def nltk_entity_analyzer(my_text):
    sentences = sent_tokenize(my_text)
    entities = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        tagged = pos_tag(words)
        entities.extend(ne_chunk(tagged))
    named_entities = [(str(entity), entity.label()) for entity in entities if isinstance(entity, nltk.Tree)]
    return named_entities

def main():
    st.title("NLPiffy with Streamlit")
    st.subheader("Natural Language Processing On the Go..")
    st.markdown("""
        #### Description
        + This is a Natural Language Processing (NLP) Based App useful for basic NLP tasks:
        Tokenization, NER, Sentiment Analysis, POS Tagging, Dependency Parsing, Summarization
        """)

    st.sidebar.header("Choose NLP Method")
    nlp_method = st.sidebar.radio("Select NLP Method", ["spaCy", "NLTK"])

    if nlp_method == "spaCy":
        nlp = spacy.load('en_core_web_sm')
    elif nlp_method == "NLTK":
        nlp = None  # Placeholder for NLTK

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
                if nlp_method == "spaCy":
                    doc = nlp(file_contents if uploaded_file is not None else user_text)
                    nlp_result = [{"Token": token.text, "Lemma": token.lemma_} for token in doc]
                elif nlp_method == "NLTK":
                    tokens = word_tokenize(file_contents if uploaded_file is not None else user_text)
                    nlp_result = [{"Token": token, "Lemma": nltk.WordNetLemmatizer().lemmatize(token)} for token in tokens]
                st.json(nlp_result)

        if st.checkbox("Show Named Entities"):
            st.subheader("Analyze Named Entities")
            if st.button("Extract Entities"):
                if nlp_method == "spaCy":
                    doc = nlp(file_contents if uploaded_file is not None else user_text)
                    entities = [(entity.text, entity.label_) for entity in doc.ents]
                elif nlp_method == "NLTK":
                    entities = nltk_entity_analyzer(file_contents if uploaded_file is not None else user_text)
                allData = ['"Token":{},\n"Entities":{}'.format(entities, entities)]
                st.json(allData)

        if st.checkbox("Show Sentiment Analysis"):
            st.subheader("Analyze Sentiment")
            if st.button("Analyze Sentiment"):
                blob = TextBlob(file_contents if uploaded_file is not None else user_text)
                sentiment = blob.sentiment
                st.success(sentiment)

        if st.checkbox("Show Part-of-Speech Tagging"):
            st.subheader("Perform Part-of-Speech Tagging")
            if st.button("Tag POS"):
                if nlp_method == "spaCy":
                    doc = nlp(file_contents if uploaded_file is not None else user_text)
                    pos_tags = [{"Token": token.text, "POS": token.pos_} for token in doc]
                elif nlp_method == "NLTK":
                     tokens = nltk.word_tokenize(file_contents if uploaded_file is not None else user_text)
                     tagged_tokens = nltk_pos_tagger(file_contents if uploaded_file is not None else user_text)
                     pos_tags = [{"Token": token, "POS": pos} for token, pos in tagged_tokens]
                     
                st.json(pos_tags)

        if st.checkbox("Show Dependency Parsing"):
            st.subheader("Perform Dependency Parsing")
            if st.button("Parse Dependencies"):
                # Add code for dependency parsing based on the selected library (spaCy or NLTK)
                if nlp_method == "spaCy":
                    doc = nlp(file_contents if uploaded_file is not None else user_text)
                    dependencies = [{"Token": token.text, "Dependency": token.dep_, "Head Token": token.head.text}
                                    for token in doc]
                    for dep in dependencies:
                        st.write(dep)
                elif nlp_method == "NLTK":
                    st.warning("Dependency Parsing is not supported with NLTK in this app.")

        if st.checkbox("Show Text Summarization"):
            st.subheader("Summarize Your Text")
            if st.button("Summarize"):
                summary_result = sumy_summarizer(file_contents if uploaded_file is not None else user_text)
                st.success(summary_result)

        # Add more checkboxes and buttons for other NLP tasks

if __name__ == '__main__':
    main()
