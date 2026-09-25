from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from .resume_parser import extract_resume_text
from .skill_extractor import extract_skills


# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_semantic_score(resume_text, job_description):

    resume_embedding = model.encode(
        [resume_text]
    )

    job_embedding = model.encode(
        [job_description]
    )

    similarity = cosine_similarity(
        resume_embedding,
        job_embedding
    )[0][0]

    score = similarity * 100

    return round(score, 2)


def calculate_skill_score(
    resume_skills,
    required_skills
):

    if not required_skills:
        return 0

    matched_skills = set(resume_skills) & set(required_skills)

    score = (
        len(matched_skills)
        / len(required_skills)
    ) * 100

    return round(score, 2)


def screen_resume(
    resume_path,
    job_description
):

    # ------------------------------------
    # Extract resume text
    # ------------------------------------

    resume_text = extract_resume_text(
        resume_path
    )

    if not resume_text.strip():
        raise ValueError(
            "Unable to extract text from resume."
        )

    # ------------------------------------
    # Extract skills
    # ------------------------------------

    resume_skills = extract_skills(
        resume_text
    )

    required_skills = extract_skills(
        job_description
    )

    # ------------------------------------
    # Semantic similarity
    # ------------------------------------

    semantic_score = calculate_semantic_score(
        resume_text,
        job_description
    )

    # ------------------------------------
    # Skill matching
    # ------------------------------------

    skill_score = calculate_skill_score(
        resume_skills,
        required_skills
    )

    # ------------------------------------
    # Final score
    # ------------------------------------

    final_score = (
        semantic_score * 0.40
        +
        skill_score * 0.60
    )

    final_score = round(
        final_score,
        2
    )

    # ------------------------------------
    # Matched / missing skills
    # ------------------------------------

    matched_skills = sorted(
        set(resume_skills) &
        set(required_skills)
    )

    missing_skills = sorted(
        set(required_skills) -
        set(resume_skills)
    )

    # ------------------------------------
    # Recommendation
    # ------------------------------------

    if final_score >= 80:
        recommendation = "Strong Match"

    elif final_score >= 60:
        recommendation = "Moderate Match"

    else:
        recommendation = "Low Match"

    return {
        "final_score": final_score,
        "semantic_score": semantic_score,
        "skill_score": skill_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "resume_skills": resume_skills,
        "required_skills": required_skills,
        "recommendation": recommendation,
    }