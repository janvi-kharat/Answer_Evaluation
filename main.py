import google.generativeai as genai
import PIL.Image
import os
import fitz
import re
import markdown2
from PIL import Image
from GetModelAns import getPointer, extract_solutions, generateAns
from Evaluation import evaluate_answer


questionPaperPDF = "QuesPdf.pdf"
studentAnswerPDF = "StudentAnsPdf.pdf"
modelAnswer = "ModelAnsPdf.pdf"

# Gemini API

map1 = {}
map2 = {}

# Function to convert PDF to images and extract text using OCR


def extract_questions_from_pdf(pdf_path):
    # Convert PDF pages to images
    pdf_document = fitz.open(pdf_path)

    for page_num in range(len(pdf_document)):
        # Extract the page
        page = pdf_document[page_num]
        # Convert the page to an image
        pix = page.get_pixmap()
        image = PIL.Image.frombytes(
            "RGB", [pix.width, pix.height], pix.samples)

        # Save the image temporarily
        image_path = f"./static/ImageData/page_{page_num + 1}.png"
        image.save(image_path)

        # Upload the image
        sample_file = genai.upload_file(
            path=image_path, display_name=f"page_{page_num + 1}.png")
        print(
            f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")

        # Choose a Gemini API model.
        model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")

        # Prompt the model with text and the previously uploaded image.
        response = model.generate_content(
            [sample_file, "Extract all questions in given image"])
        return response.text


def extract_questions(text):
    # Assuming each question starts with a number followed by a period
    # E.g., "1. What is Python?"
    import re
    pattern = r'(?:\d+\.\s*)(.*?)(?=\d+\.|$)'  # Regex to capture questions
    questions = re.findall(pattern, text, re.DOTALL)

    return [q.strip() for q in questions]


def extract_answers_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    result = []
    print(len(pdf_document))
    for page_num in range(len(pdf_document)):
        # Extract the page
        page = pdf_document[page_num]
        # Convert the page to an image
        pix = page.get_pixmap()
        image = PIL.Image.frombytes(
            "RGB", [pix.width, pix.height], pix.samples)

        # Save the image temporarily
        image_path = f"./static/ImageData/page_{page_num + 1}.png"
        image.save(image_path)

        # Upload the image
        sample_file = genai.upload_file(
            path=image_path, display_name=f"page_{page_num + 1}.png")
        print(
            f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")

        # Choose a Gemini API model.
        model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")

        # Prompt the model with text and the previously uploaded image.
        response = model.generate_content(
            [sample_file, "Extract only handwritten text precisely"])
        result.append(response.text)
    return result
#


def remove_markdown(text):
    import re

    # Remove Markdown symbols for headers, bold, italics, etc.
    clean_text = re.sub(r'[#*\-_>`~]', '', text)  # Removes *, #, -, _, >, `, ~

    # Remove Markdown links/images ![alt](url) and [text](url)
    clean_text = re.sub(r'!\[.*?\]\(.*?\)', '', clean_text)  # Removes images
    clean_text = re.sub(r'\[.*?\]\(.*?\)', '', clean_text)  # Removes links

    # Remove backticks for inline code or code blocks
    # Removes inline code or code blocks
    clean_text = re.sub(r'`{1,3}[^`]*`{1,3}', '', clean_text)

    # Clean up extra whitespaces
    clean_text = clean_text.strip()

    return clean_text


# -----------------------------------------------------------------------------------------------
questions = extract_questions_from_pdf("QuesPdf.pdf")
# print(questions)
quesArray = extract_questions(questions)
# print(quesArray)
studentAnswer = extract_answers_from_pdf("StudentAnsPdf.pdf")

for i in range(len(quesArray)):
    map2[quesArray[i]] = studentAnswer[i]

print(map2)

# Map2 Created Now Map1 Remaining
pointers = getPointer("ModelAnsPdf.pdf")
# print(pointers)
pointerArr = extract_solutions(pointers)
ModelAns = generateAns(pointerArr, quesArray)


for i in range(len(ModelAns)):
    text = remove_markdown(ModelAns[i])
    ModelAns[i] = text

# for i in ModelAns:
#     print(i)


for i in range(len(quesArray)):
    map1[quesArray[i]] = ModelAns[i]

print(map1)

finalScore = 0

for i in range(len(map1)):
    print("Question : {i}")
    total, grammer, spell = evaluate_answer(
        5, map1[quesArray[i]], map2[quesArray[i]])
    print(f"Spell : {spell}")
    print("Grammer : {grammer} ")
    print("Total : {total}")
    finalScore += total

print(finalScore)
