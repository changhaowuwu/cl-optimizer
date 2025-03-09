import fitz  # PyMuPDF for PDF handling
import google.generativeai as genai

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text("text") for page in doc])
    print(text)

    return text

def optimize_cover_letter(cover_letter):
    # Set your Gemini API key
    GENAI_API_KEY = "AIzaSyAkbEE0b7IUYFR3jxt5LQwN645pYHivj1Y"
    genai.configure(api_key=GENAI_API_KEY)
    """Optimize cover letter using Google Gemini API."""
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    prompt = f"""
    I have written a cover letter for a Junior software engineer position at UBS. Please optimize it for clarity, conciseness, and impact while maintaining a professional and engaging tone. Ensure it highlights my most relevant skills and experiences effectively. Output only the improved cover letter without any explanations or additional commentary:
    "{cover_letter}"
    """
    response = model.generate_content(prompt)
    print(response.text)
    return response.text if response.text else "Error optimizing cover letter."

def save_text_to_pdf(text, output_pdf):
    """Save text as a new PDF file."""
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), text)  # Insert optimized text at position (50,50)
    doc.save(output_pdf)
    print(f"Optimized cover letter saved as: {output_pdf}")

# Example Usage
input_pdf = "Cover_letter.pdf"
output_pdf = "optimized_cover_letter.pdf"

original_text = extract_text_from_pdf(input_pdf)
optimized_text = optimize_cover_letter(original_text)
save_text_to_pdf(optimized_text, output_pdf)
