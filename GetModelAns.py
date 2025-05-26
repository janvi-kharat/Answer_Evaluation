import google.generativeai as genai
import PIL.Image
import os
import fitz
import re
import markdown2
from PIL import Image
from groq import Groq

import os

from groq import Groq

client = Groq(
    api_key="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"
)


genai.configure(api_key="AIzaSyAXpLXA1C5PfXho49tzDxjEI2LJ23uoWwQ")
def getPointer(pdf_path):
    pdf_document = fitz.open(pdf_path)
    pointers = ""

    for page_num in range(len(pdf_document)):
        # Extract the page
        page = pdf_document[page_num]
        # Convert the page to an image
        pix = page.get_pixmap()
        image = PIL.Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Save the image temporarily
        image_path = f"./static/ImageData/page_{page_num + 1}.png"
        image.save(image_path)

        # Upload the image
        sample_file = genai.upload_file(path=image_path, display_name=f"page_{page_num + 1}.png")
        print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")

        # Choose a Gemini API model.
        model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")

        # Prompt the model with text and the previously uploaded image.
        response = model.generate_content([sample_file, "Extract all solution text from given image"])
        pointers+=response.text
    return pointers

# pointers = getPointer("ModelAnsPdf.pdf")


def extract_solutions(text):
    # Import regular expressions library
    import re

    # Regex pattern to capture everything after "Solution:" in each line
    pattern = r'Solution:\s*(.*?)(?=Solution:|$)'  # Capture solution text after "Solution:"
    solutions = re.findall(pattern, text, re.DOTALL)  # Extract the solutions

    # Clean up the extracted solutions by stripping and removing '\n' and '-'
    cleaned_solutions = [sol.replace('\n', ' ').replace('-', '').strip() for sol in solutions]

    return cleaned_solutions



# pointerArr = extract_solutions(pointers)
# print(pointerArr)


def generateAns(pointerArr,quesArr):
    answerArr = []

    for i in range(len(quesArr)):
        prompt = "the question is "+quesArr[i]+" give me answer for this question using following pointers pointers = "+pointerArr[i]+" please only give answer and do not repeat the questions"
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="gemma2-9b-it",
        )

        answerArr.append(chat_completion.choices[0].message.content)
    return answerArr




