import streamlit as st
from pybart import api as bart
    

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


def main():
    nlp, displacy = load("en_ud_model_lg")

    option = st.sidebar.selectbox(
            'Choose a ready to use example',
            ('', 'The quick brown fox jumped over the lazy dog.', 'The sheriff was shot by Bob.', 'Bob saw a cat, while driving a car.'))

    answer = st.text_input('Enter a sentence:', value=option)


    if answer:
        doc = nlp(answer)
        d = {}
        for t_son in doc:
            for t_par in t_son._.parent_list:
                if "nsubj" == t_par["rel"]:
                    d[(t_par['head'].i, t_par['head'].text, t_par['head'].tag_.startswith("VB"))] = [t_son.text] + ([] if (t_par['head'].i, t_par['head'].text, t_par['head'].tag_.startswith("VB")) not in d else d[(t_par['head'].i, t_par['head'].text, t_par['head'].tag_.startswith("VB"))])


        for pred_triplet, pred_vals in d.items():
            st.write('Q: who', 'is' if not pred_triplet[2] else "", pred_triplet[1], '? A: ', ", ".join(pred_vals))
        
        
        #displacy.serve(doc, style='dep')


if __name__ == "__main__":
    main()

