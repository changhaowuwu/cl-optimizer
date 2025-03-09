from typing import Dict

import google.generativeai as genai


def generate_cover_letter(job_link: str) -> Dict[str, any]:
    """
    Generate a cover letter based on the job link context

    Args:
        job_link: URL of the job posting

    Returns:
        dict: Contains success status and either cover letter or error message
    """
    try:
        # Create prompt for cover letter generation
        prompt = f"""
        You are a professional cover letter writer. Create a compelling cover letter for a software engineering position.

        The position is for this job posting: {job_link}

        Write a professional cover letter that:
        1. Has a formal business letter format
        2. Shows enthusiasm for the role and company
        3. Mentions key software engineering skills (full-stack development, Java, Python, React, etc.)
        4. Highlights leadership and team collaboration experience
        5. Demonstrates problem-solving abilities and technical expertise
        6. Includes:
           - Professional greeting
           - 3-4 strong paragraphs
           - Professional closing
           - Proper spacing and formatting

        Keep the tone professional but enthusiastic. Focus on full-stack development, software architecture, 
        and team leadership capabilities.
        """

        # Generate cover letter
        model = genai.GenerativeModel("gemini-pro")
        GENAI_API_KEY = "AIzaSyAkbEE0b7IUYFR3jxt5LQwN645pYHivj1Y"
        genai.configure(api_key=GENAI_API_KEY)
        model_config = {
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 2048,
        }
        response = model.generate_content(prompt, generation_config=model_config)

        if response and response.text:
            return {"success": True, "cover_letter": response.text.strip()}
        else:
            return {"success": False, "error": "Failed to generate cover letter"}

    except Exception as e:
        return {"success": False, "error": f"Error generating cover letter: {str(e)}"}
    
if __name__ == "__main__":
    # Code to execute when the script runs directly
    print(generate_cover_letter("https://www.linkedin.com/jobs/view/4169523845/?alternateChannel=search&refId=WTYwK%2BKfaV6A80EgvVH1LA%3D%3D&trackingId=sc5o4CNLmThqtBOkNok6gw%3D%3D"))
