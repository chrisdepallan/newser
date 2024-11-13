from flask import render_template
from app import app, collection_articles, collection_user_registration, collection_comments
from flask import request,requests,jsonify

@app.route("/api")
def api():
    return render_template('api/api_index.html')

@app.route("/api/process", methods=['GET'])
def process_article():
    article_url = request.args.get('articleurl')
    command = request.args.get('command')

    if not article_url or not command:
        return jsonify({"error": "Missing articleurl or command parameter"}), 400

    if command == "summary":
        # Get article text from URL
        try:
            # Call Hugging Face API for summarization
            api_url = 'https://api-inference.huggingface.co/models/facebook/bart-large-cnn'
            api_key = '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'
            
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            # Get text from article URL
            # Note: You'll need to implement get_article_text() to extract text from URL
            article_text = get_article_text(article_url)
            
            response = requests.post(
                api_url,
                headers=headers,
                json={'inputs': article_text}
            )
            
            summary = response.json()[0]['summary_text']
            result = {'summary': summary}
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
            
    # elif command == "keywords":
    #     # Call the keywords function (you'll need to implement this)
    #     result = extract_keywords(article_url)
    else:
        return jsonify({"error": "Invalid command"}), 400

    return jsonify(result)