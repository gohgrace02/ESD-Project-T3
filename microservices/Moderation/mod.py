from flask import Flask, request, jsonify
import re

app = Flask(__name__)

def load_vulgarity_list():
  # Replace this with your logic to load the vulgarity list (e.g., from file, database)
  return ["stupid", "bitch", "cock"]

def is_vulgar(text):
  """Checks if the provided text contains vulgar language.

  Args:
      text: The text to check for vulgarity.

  Returns:
      True if the text contains vulgar language, False otherwise.
  """
  text = text.lower()
  text = re.sub(r"[^\w\s]", "", text)  # Remove punctuation
  vulgarity_list = load_vulgarity_list()

  for word in text.split():
    if word in vulgarity_list:
      return True

  return False

@app.route("/check_vulgarity", methods=["POST"])
def check_vulgarity():
  text = request.json.get("text")
  if not text:
      return jsonify({"error": "Missing text data in request body"}), 400

  if is_vulgar(text):
    return jsonify({"vulgar": True})
  else:
    return jsonify({"vulgar": False})

if __name__ == "__main__":
  app.run(debug=True)
