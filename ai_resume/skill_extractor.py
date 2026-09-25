import re


SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "javascript",
    "sql",
    "mysql",
    "mongodb",
    "pandas",
    "numpy",
    "excel",
    "power bi",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "natural language processing",
    "nlp",
    "computer vision",
    "tensorflow",
    "keras",
    "pytorch",
    "scikit-learn",
    "flask",
    "django",
    "react",
    "html",
    "css",
    "transformers",
    "bert",
    "llm",
    "rag",
    "langchain",
    "git",
    "github",
    "docker",
    "aws",
    "azure"
]


def extract_skills(text):
    if not text:
        return []

    text = text.lower()
    found_skills = []

    for skill in SKILLS:
        skill_pattern = r'(?<!\w)' + re.escape(skill.lower()) + r'(?!\w)'

        if re.search(skill_pattern, text):
            found_skills.append(skill)

    return sorted(set(found_skills))