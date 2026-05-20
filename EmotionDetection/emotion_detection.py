import requests

def emotion_detector(text_to_analyze: str) -> dict:
    """
    Analyze the emotions in the given text using the Watson NLP API.

    Args:
        text_to_analyze (str): The input text to analyze.

    Returns:
        dict: A dictionary containing emotion scores and the dominant emotion,
              or an error message if something goes wrong.
    """

    url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    body = {
        "raw_document": {
            "text": text_to_analyze
        }
    }

    try:
        response = requests.post(url, headers=headers, json=body, timeout=10)
        response.raise_for_status()
        data = response.json()

        emotion_predictions = data.get("emotionPredictions")
        if not emotion_predictions:
            return {"error": "Missing or empty 'emotionPredictions' in response."}

        first_prediction = emotion_predictions[0]
        emotions = first_prediction.get("emotion")
        if not emotions:
            return {"error": "Missing 'emotion' in response."}

        dominant_emotion = max(emotions, key=emotions.get)

        return {
            **emotions,
            "dominant_emotion": dominant_emotion
        }

   
    except (
        requests.exceptions.HTTPError, 
        requests.exceptions.ConnectionError, 
        requests.exceptions.Timeout,
        requests.exceptions.RequestException

    ) as e:
        return {"error": f"Request failed: {str(e)}"}

    except KeyError as e:
        return {"error": f"Missing key in response: {e}"}

    except IndexError as e:
        return {"error": f"Missing list item in response: {e}"}

    except ValueError:
        return {"error": "Invalid JSON response."}

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}