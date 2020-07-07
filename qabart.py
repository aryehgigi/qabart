import streamlit as st
from pybart import api as bart
from pattern.en import conjugate


@st.cache(allow_output_mutation=True)
def load(module):
    print("importing spacy")
    import spacy
    print("loading module")
    inner_nlp = spacy.load(module)
    print("finished")
    con = bart.Converter()
    inner_nlp.add_pipe(con, "BART")
    return inner_nlp, spacy.displacy


examples = {
    '':'',
    'adjective-predicate':'The quick brown fox jumped over the lazy dog.',
    'passive':'The sheriff was shot by Bob.',
    'adverbial-clauses': 'Bob saw a cat, while driving a car.', 
    'elaboration': 'I like fruits such as apples, bananas and oranges.',
    'copula1': "He is the president."}


def main():
    nlp, displacy = load("en_ud_model_lg")

    option = st.sidebar.selectbox(
            'Choose a ready to use example',
            ('', 'adjective-predicate', 'passive', 'adverbial-clauses', 'elaboration', 'copula1'))

    answer = st.text_input('Enter a sentence:', value=examples[option])


    if answer:
        doc = nlp(answer)
        d_subj = {}
        d_obj = {}
        for t_son in doc:
            for t_par in t_son._.parent_list:
                if "nsubj" == t_par["rel"]:
                    d_subj[(t_par['head'].i, t_par['head'].text, t_par['head'].tag_.startswith("VB"))] = [t_son.text] + ([] if (t_par['head'].i, t_par['head'].text, t_par['head'].tag_.startswith("VB")) not in d_subj else d_subj[(t_par['head'].i, t_par['head'].text, t_par['head'].tag_.startswith("VB"))])
                if "dobj" == t_par["rel"]:
                    d_obj[(t_par['head'].i, t_par['head'].text, t_par['head'].tag_.startswith("VB"))] = [t_son.text] + ([] if (t_par['head'].i, t_par['head'].text, t_par['head'].tag_.startswith("VB")) not in d_obj else d_obj[(t_par['head'].i, t_par['head'].text, t_par['head'].tag_.startswith("VB"))])
        
        if len(d_subj) != 0 or len(d_obj) != 0:
            for pred_triplet, pred_vals in d_subj.items():
                st.write('Q: who', 'is' if not pred_triplet[2] else "", pred_triplet[1], '? A: ', ", ".join(pred_vals))
            for pred_triplet, pred_vals in d_obj.items():
                st.write('Q: who/what', 'was' if pred_triplet[2] else "", conjugate(pred_triplet[1], tense='ppart'), '? A: ', ", ".join(pred_vals))
        else:
            st.write("Nothing to show..")
        
        #displacy.serve(doc, style='dep')


if __name__ == "__main__":
    main()

