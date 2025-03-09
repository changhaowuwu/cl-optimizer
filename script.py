import os
from pdfminer.high_level import extract_text

cover_letter_file = extract_text("Cover_letter.pdf")
template_file = os.getcwd() +  "\\template.tex"
coverletter_file = os.getcwd() +  "\\coverletter.tex"

print(cover_letter_file)