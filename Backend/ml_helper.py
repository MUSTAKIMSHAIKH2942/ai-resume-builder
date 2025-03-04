from transformers import pipeline

# Load a pre-trained summarization model from Hugging Face
summarizer = pipeline('summarization')

def generate_resume_suggestions(resume):
    # Combine resume sections into a single text
    text = f"Education: {' '.join(resume['education'])}\nExperience: {' '.join(resume['experience'])}\nSkills: {' '.join(resume['skills'])}"

    # Generate suggestions using the summarization model
    suggestions = summarizer(text, max_length=50, min_length=25, do_sample=False)
    return suggestions[0]['summary_text']