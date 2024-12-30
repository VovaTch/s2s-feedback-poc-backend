def get_feedback_request(eng_sentence: str, lang_sentence: str, lang: str) -> str:
    return f"""
    The english sentence is "{eng_sentence}" and the {lang} sentence is "{lang_sentence}". Please provide
    feedback for the translation.
    """
