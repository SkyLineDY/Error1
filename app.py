from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_answer_from_model(question):
    # Замените YOUR_API_KEY на ваш реальный API-ключ
    api_key = "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"
    
    # URL API языковой модели
    url = "deepseek/deepseek-r1-distill-qwen-1.5b"

    # Параметры запроса
    payload = {
        "prompt": question,
        "max_tokens": 50,  # Максимальное количество токенов в ответе
        "temperature": 0.7  # Температура генерации текста
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Проверка на ошибки в ответе
        answer = response.json().get('text', "No answer received")
        return answer
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return "Error occurred while fetching the answer from the model."

@app.route('/api/request', methods=['POST'])
def handle_request():
    data = request.json
    question = data.get('query')
    id = data.get('id')

    if not question or not id:
        return jsonify({"error": "Invalid request"}), 400

    answer = get_answer_from_model(question)
    reasoning = "Reasoning based on the language model."
    sources = ["https://itmo.ru/ru/news/", "https://itmo.ru/ru/news/"]

    response = {
        "id": id,
        "answer": answer,
        "reasoning": reasoning,
        "sources": sources
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    