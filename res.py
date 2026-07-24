from pypdf import PdfReader
import ollama


def pdf_reader(file="Untitled design.pdf"):
    try:
        reader = PdfReader(file)
        text = reader.pages[0].extract_text()
        return text
    except Exception as error:
        print(f"Failed to read the file. Error: {error}")
        return None


def rating(text=None):
    if text is None:
        text = pdf_reader()
    if text is None:
        return None

    m = "llama3.2"
    commands = [
        {"role": "system", "content": "Based off of the text you are given which is a resume, give a score from 1 to 10 on how good the candidate would be for an AI Engineer role. Consider their past experience and skills. Only respond with a single number between 1 and 10, nothing else."},
        {"role": "user", "content": text}
    ]

    try:
        response = ollama.chat(model=m, messages=commands)
        return response.message.content.strip()
    except Exception as error:
        print(f"The AI failed before completing prompt. Error: {error}")
        return None


def main():
    score_text = rating()
    if score_text is None:
        print("Something went wrong. Please try again later.")
        return

    try:
        score = int(score_text)
        if 0 <= score <= 10:
            print(score)
        else:
            print(f"Unexpected score value: {score_text}")
    except ValueError:
        print(f"Could not parse score: {score_text}")


if __name__ == "__main__":
    main()
