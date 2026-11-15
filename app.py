from flask import Flask, render_template, request, jsonify
import requests
app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    text = data.get("text", "")
    source = data.get("source", "")
    target = data.get("target", "")
    if not text.strip():
        return jsonify({"error": "Please enter some text."}), 400
    if source == target:
        return jsonify({"translation": text})
    try:
        response = requests.get(
            "https://api.mymemory.translated.net/get",
            params={
                "q": text,
                "langpair": f"{source}|{target}"
            },
            timeout=15
        )
        response.raise_for_status()
        result = response.json()
        if result.get("responseStatus") != 200:
            return jsonify({"error": "Translation service failed."}), 502
        translated_text = result["responseData"]["translatedText"]
        return jsonify({"translation": translated_text})
    except requests.RequestException:
        return jsonify({"error": "Unable to connect to translation service."}), 503
    except (KeyError, ValueError):
        return jsonify({"error": "Invalid translation response."}), 502
if __name__ == "__main__":
    app.run(debug=True)
