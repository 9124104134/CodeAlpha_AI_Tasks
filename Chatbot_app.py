import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


st.set_page_config(page_title="FAQ AI Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 Intelligent FAQ Chatbot")
st.write("Ask me anything about our services, and I will find the best match!")


faq_data = [
    {
        "question": "What is Artificial Intelligence?",
        "answer": "Artificial Intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think like humans and mimic their actions."
    },
    {
        "question": "How do I start learning machine learning?",
        "answer": "To start learning machine learning, it is best to learn Python programming, pick up foundational math (linear algebra, calculus, statistics), and explore libraries like Scikit-Learn, TensorFlow, or PyTorch."
    },
    {
        "question": "What is Cloud Computing?",
        "answer": "Cloud computing is the delivery of computing services—including servers, storage, databases, networking, software, and analytics—over the Internet ('the cloud')."
    },
    {
        "question": "What is Retrieval-Augmented Generation (RAG)?",
        "answer": "RAG is an AI framework for improving the quality of LLM-generated responses by grounding the model on external sources of knowledge before generating a response."
    },
    {
        "question": "How can I contact support?",
        "answer": "You can reach out to our official support channel via email at services@codealpha.tech or connect with us on WhatsApp."
    }
]


faq_questions = [item["question"] for item in faq_data]
faq_answers = [item["answer"] for item in faq_data]


def get_best_response(user_query, questions, answers, threshold=0.25):
   
    all_texts = questions + [user_query]
    
    
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
 
    faq_vectors = tfidf_matrix[:-1]
    query_vector = tfidf_matrix[-1]
    

    similarities = cosine_similarity(query_vector, faq_vectors).flatten()
    
    
    best_match_idx = np.argmax(similarities)
    highest_score = similarities[best_match_idx]
    
    
    if highest_score >= threshold:
        return answers[best_match_idx], highest_score
    else:
        return "I'm sorry, I couldn't find a close match for your question in my FAQ database. Could you try rephrasing it?", highest_score


if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your AI Assistant. Ask me any question from the FAQ database!"}
    ]


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Type your question here..."):
    
    with st.chat_message("user"):
        st.markdown(user_input)
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    
    bot_response, score = get_best_response(user_input, faq_questions, faq_answers)
    
    
    with st.chat_message("assistant"):
        st.markdown(bot_response)
        
        if score >= 0.25:
            st.caption(f"Match Confidence: {score:.2f}")
            
   
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

st.markdown("---")
st.caption("CodeAlpha AI Internship - Task 2 | Built with Streamlit & Scikit-Learn")
