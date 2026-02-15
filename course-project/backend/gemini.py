from google import genai
import os
from dotenv import load_dotenv
import json

load_dotenv()


class Gemini:
    def __init__(self):
        # Create a client using the new google-genai SDK
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_id = "gemini-2.5-flash"

    def generate_content(self, content):
        # New SDK syntax for generating content
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=content,
            config={"response_mime_type": "application/json"},
        )
        return response

    def recommend_class(
        self, user_info=None, class_info=None, specialization_requirements=None
    ):
        print("Gemini being called: recomending a class")
        prompt = f"""### SYSTEM ROLE
            You are the UCI ICS Academic Adviser. You are an expert in the UC Irvine Information and Computer Sciences curriculum. Your goal is to recommend the single best course for a student based on their academic history, interests, and projected course load.

            ### RAW STUDENT DATA
            The following is the student's current profile in JSON format:
            <student_json>
            {user_info}
            </student_json>

            If there is no student profile, just recommend 4 classes that you think a student should take.

            ### EXTERNAL CONTEXT
            <specialization_requirements>
            {specialization_requirements}
            </specialization_requirements>

            <course_catalog_and_reviews>
            {class_info}
            </course_catalog_and_reviews>

            ### SPECIFIC GOAL
            [USER_DEFINED_GOALS_PLACEHOLDER]

            ### OPERATIONAL GUIDELINES
            1. DATA EXTRACTION: Parse the `completedClasses` array. Note that the student has already taken these courses; do NOT recommend them. Only valid if there is a student profile. Do NOT recommend a course where the student has not completed all its prerequisites.
            2. INTEREST ANALYSIS: Look at the `interests` list. These are areas where the student has expressed specific interest. Cross-reference this with the `grade` received in `completedClasses` (e.g., an A- in a difficulty 3 class indicates high aptitude in that subject). Only valid if there is a student profile.
            3. ALIGNMENT: Prioritize courses from the <specialization_requirements> that match the student's specialization (e.g., "specialization"). Only valid if there is a student profile.
            4. FURTHER ALIGNMENT: Take into account the "quartersLeft" and "coursesLeft" field in the student profile. If the student is on "crunch time" (e.g., quartersLeft=1 and coursesLeft=3), prioritize easier courses that are more likely to be successfully completed. Only valid if there is a student profile.
            5. REVIEW CHECK: Scan <course_catalog_and_reviews> for positive peer feedback to ensure a high-quality student experience.

            ### CONSTRAINTS
            - Return ONLY a valid JSON object.
            - Strictly ground your recommendation in the provided catalog.
            - you should only output a maximum of 4 classes

            ### FINAL EXECUTION
            Based on the student profile provided in the JSON, recommend one course.

            Expected JSON Output:

            [{{
            "id": "the class id",
            "title": "the class title"
            }}]
            """


        response = self.generate_content(prompt)
        return json.loads(response.text)


# just testing
if __name__ == "__main__":
    gemini = Gemini()
    data = {
        "completedClasses": [{"className": "CS 161", "grade": "A-", "difficulty": 3}],
        "strengths": {
            "Math": 3,
            "Algorithms": 3,
            "Data Structures": 3,
            "Programming": 3,
            "Recursion": 3,
        },
        "username": "nathan",
        "quartersLeft": 4,
        "specialization": "Algorithms",
    }

    # Passing dummy values for context for testing
    response = gemini.recommend_class(
        data,
        "CS 122A: Intro to Databases",
        "Specialization: Algorithms requires CS 161, CS 162",
    )
    print(response)
