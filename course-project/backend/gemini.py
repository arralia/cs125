from google import genai
import os
from dotenv import load_dotenv

load_dotenv()


class Gemini:
    def __init__(self):
        # Create a client using the new google-genai SDK
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_id = "gemini-2.5-flash"

    def generate_content(self, content):
        # New SDK syntax for generating content
        response = self.client.models.generate_content(
            model=self.model_id, contents=content
        )
        return response

    def recomend_class(
        self, user_info, class_info=None, specialization_requirements=None
    ):
        prompt = f"""### SYSTEM ROLE
            You are the UCI ICS Academic Adviser. You are an expert in the UC Irvine Information and Computer Sciences curriculum. Your goal is to recommend the single best course for a student based on their academic history and self-reported strengths.

            ### RAW STUDENT DATA
            The following is the student's current profile in JSON format:
            <student_json>
            {user_info}
            </student_json>

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
            1. DATA EXTRACTION: Parse the `completedClasses` array. Note that the student has already taken these courses; do NOT recommend them.
            2. STRENGTH ANALYSIS: Look at the `strengths` object. A value of 1-3 indicates areas where the student feels capable or neutral. Cross-reference this with the `grade` received in `completedClasses` (e.g., an A- in a difficulty 3 class indicates high aptitude).
            3. ALIGNMENT: Prioritize courses from the <specialization_requirements> that match the student's specialization (e.g., "{{specialization}}").
            4. REVIEW CHECK: Scan <course_catalog_and_reviews> for positive peer feedback to ensure a high-quality student experience.

            ### CONSTRAINTS
            - Return ONLY a valid JSON object.
            - Strictly ground your recommendation in the provided catalog.

            ### FINAL EXECUTION
            Based on the student profile provided in the JSON, recommend one course.

            Expected JSON Output:
            {{
            "id": "the class id",
            "title" "the class title"
            }}

            The JSON output should be the same as the input for the class catalog we provide
            """

        return self.generate_content(prompt)


# just a test here
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
    response = gemini.recomend_class(
        data,
        "CS 122A: Intro to Databases",
        "Specialization: Algorithms requires CS 161, CS 162",
    )
    print(response.text)
