from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
 
# Настройки API Hugging Face
API_URL = "https://api-inference.huggingface.co/models/gpt2"
API_TOKEN = "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"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def generate_response(query):
    """
    Генерация ответа через API Hugging Face.
    """
    options = [line.split(". ")[1] for line in query.split("\n") if line.strip().isdigit()]
    prompt = f"Ответь на вопрос: {query}. Выбери правильный вариант из предложенных."

    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    if response.status_code == 200:
        raw_response = response.json()[0]['generated_text']
        reasoning = raw_response.split("Ответ:")[0].strip()
        answer = extract_answer(raw_response, options)
        return {
            "answer": answer,
            "reasoning": reasoning,
            "sources": []
        }
    else:
        raise Exception(f"Ошибка при обращении к API: {response.status_code}, {response.text}")

def extract_answer(response, options):
    """
    Извлечение номера правильного ответа.
    """
    for i, option in enumerate(options, start=1):
        if option.lower() in response.lower():
            return i
    return None

@app.route('/api/request', methods=['POST'])
def handle_request():
    data = request.json
    query = data.get("query", "")
    request_id = data.get("id", 0)

    try:
        result = generate_response(query)
        result["id"] = request_id
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "id": request_id,
            "answer": None,
            "reasoning": str(e),
            "sources": []
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
