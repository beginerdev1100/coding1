from flask import Flask, request, render_template
from res import pdf_reader, rating

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    score = None
    error = None

    if request.method == "POST":
        file = request.files.get("resume")
        if not file or file.filename == "":
            error = "Please upload a PDF file."
        else:
            text = pdf_reader(file)
            if text is None:
                error = "Could not read the PDF. Make sure it contains selectable text."
            else:
                score_text = rating(text)
                if score_text is None:
                    error = "The AI failed to respond. Is Ollama running?"
                else:
                    try:
                        score = int(score_text)
                        if not (0 <= score <= 10):
                            error = f"Unexpected score: {score_text}"
                            score = None
                    except ValueError:
                        error = f"Could not parse score: {score_text}"

    return render_template("index.html", score=score, error=error)


if __name__ == "__main__":
    app.run(debug=True)
