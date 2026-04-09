from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(resume_text, job_desc):
    try:
        tfidf = TfidfVectorizer(stop_words="english")
        matrix = tfidf.fit_transform([resume_text, job_desc])
        similarity = cosine_similarity(matrix)[0][1]
        return round(similarity * 100, 2)
    except:
        return 0.0