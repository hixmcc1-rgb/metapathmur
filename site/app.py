import streamlit as st
from Bio import Entrez

# Укажи свой email для API PubMed (требуется)
Entrez.email = "your_email@example.com"

def search_pubmed(query, max_results=10):
    """Ищем статьи в PubMed по ключевому слову"""
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    ids = record["IdList"]

    results = []
    for pmid in ids:
        summary = Entrez.esummary(db="pubmed", id=pmid)
        doc = Entrez.read(summary)
        title = doc[0]["Title"]
        journal = doc[0].get("FullJournalName", "Unknown journal")
        pubdate = doc[0].get("PubDate", "Unknown date")
        results.append((title, journal, pubdate, pmid))
    return results

# Streamlit интерфейс
st.title("🧬 Metabolic Pathway Hypothesis Explorer")
st.write("Введите название метаболита, фермента или процесса — и получите статьи из PubMed")

query = st.text_input("🔍 Введите запрос (например: glutamine, glycolysis, krebs cycle):")

if st.button("Искать"):
    if query.strip() != "":
        with st.spinner("Ищем в PubMed..."):
            try:
                results = search_pubmed(query)
                if results:
                    st.success(f"Найдено {len(results)} статей:")
                    for i, (title, journal, pubdate, pmid) in enumerate(results, 1):
                        st.markdown(f"**{i}. {title}**  \n*{journal}, {pubdate}*  \n[PMID:{pmid}](https://pubmed.ncbi.nlm.nih.gov/{pmid}/)")
                else:
                    st.warning("Ничего не найдено. Попробуйте другой запрос.")
            except Exception as e:
                st.error(f"Ошибка: {e}")
    else:
        st.warning("Введите поисковый запрос!")






























