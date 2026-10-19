import google.generativeai as genai


def chatbot_response(message, api_key):

    if not api_key:
        return "GEMINI_API_KEY is missing."

    try:

        genai.configure(api_key=api_key)

        model = genai.GenerativeModel(
            'gemini-3.5-flash-lite'
        )

        response = model.generate_content(
            message
        )

        return response.text

    except Exception as e:

        return f"Chatbot Error: {str(e)}"