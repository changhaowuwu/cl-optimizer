import os, subprocess
import fileinput
import shutil
import google.generativeai as genai
from pdfminer.high_level import extract_text

def gemini_get(prompt, model="gemini-2.0-flash"):
    GENAI_API_KEY = "AIzaSyAkbEE0b7IUYFR3jxt5LQwN645pYHivj1y" # TODO: Set api key to env/config file
    genai.configure(api_key=GENAI_API_KEY)
    model = genai.GenerativeModel(model)
    response = model.generate_content(prompt)
    print(response.text)
    return response.text if response.text else "Error optimizing cover letter."

def get_cl_optimizer_prompt(coverletter_text):
    return "I have written a cover letter for a " \
    "Junior software engineer position at UBS. " \
    "Please optimize it for clarity, conciseness, and impact while maintaining a professional and engaging tone. " \
    "Ensure it highlights my most relevant skills and experiences effectively. " \
    "Output only the improved cover letter without any explanations or additional commentary:" \
    f"The cover letter to improve is:{coverletter_text}"


def replace_value(line, field, value):
    if field in line:
        line = line.replace(field, value)
    return line

def generateCoverLetter(job_listing, company_name, address1, address2):
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # read user credentials from file
    """api_key_file = os.path.join(script_dir, "login")
    with open(api_key_file, "r") as f:
        user_email = f.readline().strip()
        #user_password = f.readline().strip()"""

    # read settings from file
    settings_file = os.path.join(script_dir, "settings")
    with open(settings_file, "r") as f:
        first_name = f.readline().strip()
        last_name = f.readline().strip()
        website_url = f.readline().strip()
        email = f.readline().strip()
        phone_number = f.readline().strip()

    # read resume from file
    """rawresume_file = os.path.join(script_dir, "rawresume")
    if os.path.exists(rawresume_file):
        with open(rawresume_file, "r", encoding="UTF-8", errors='ignore') as f:
            resume = f.read()
        message = "Write a cover letter without a letter closing for this job position: " + company_name + " " + job_listing + "\n This is my resume: \n" + resume
        message = "".join(c for c in message if c <= "\uFFFF")
    else:
        message = "Write a cover letter without a letter closing for this job position: " + company_name + " " + job_listing
    print(message)"""

    content = gemini_get(get_cl_optimizer_prompt(extract_text("Cover_letter.pdf")))

    print(content) 

    paragraphs = content.split("\n\n")

    template_file = os.path.join(script_dir, "template.tex")
    coverletter_file = os.path.join(script_dir, "coverletter.tex")
    shutil.copyfile(template_file, coverletter_file)

    for line in fileinput.input(coverletter_file, inplace=True):
        switch = {
            "#firstName": first_name,
            "#lastName": last_name,
            "#websiteUrl": website_url,
            "#email": email,
            "#phoneNumber": phone_number,
            "#fullName": first_name + " " + last_name,
            "#address1": address1,
            "#address2": address2,
            "#companyName": company_name
        }
        for field, value in switch.items():
            line = replace_value(line, field, value)
        print(line, end='')

    for i in range(1, len(paragraphs) - 1):
        # ignore sincerely when it is not in the same paragraph as applicant name (pretty often)
        if "Sincerely," in paragraphs[i]:
            continue
        file_path = os.path.join(script_dir, "coverletter.tex")
        for line in fileinput.input(file_path, inplace=True, backup=".bak"):
            if line.strip() == "\\vspace{0.5cm}":
                print("\\lettercontent{" + paragraphs[i] + "}")
            print(line, end='')

    print("----------------------1-------------------------")
    #current_dir = os.getcwd()
    print("----------------------2---------------------------")
    #os.chdir(script_dir)
    print("----------------------3---------------------------")
    print(coverletter_file)
    subprocess.run(["xelatex", "-interaction=batchmode", coverletter_file])
    #compile_latex(coverletter_file)
    print("----------------------4---------------------------")
    #os.chdir(current_dir)

def compile_latex(latex_file):
    try:
        # Run pdflatex (you can change the command if you are using a different LaTeX compiler)
        subprocess.run(['xelatex', latex_file], check=True)
        print("LaTeX document compiled successfully!")
    except subprocess.CalledProcessError:
        print("Error in compiling the LaTeX document!")

generateCoverLetter("NULL","UBS","Bahnhofstrasse 45","8001 Zurich, Switzerland")