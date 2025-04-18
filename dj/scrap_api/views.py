import os
import sys
scraper_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../scraper'))
if scraper_path not in sys.path:
    sys.path.insert(0, scraper_path)
import csv
from live_match_scraper import LiveMatchStats
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse, Http404
from django.conf import settings
import google.generativeai as genai

from rest_framework.decorators import api_view

class LiveCricketStatsView(APIView):
    def get(self, request):
        data = LiveMatchStats().get_Stats()
        if "error" in data:
            return Response({"error": data["error"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data, status=status.HTTP_200_OK)

def get_commentary(request, code):
    data_dir = os.path.join(settings.BASE_DIR, 'data')
    file_path = os.path.join(data_dir, f"{code}.csv")

    if not os.path.exists(file_path):
        raise Http404("Match commentary not found.")

    commentary = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            commentary.append({
                "ball": row["Ball"],
                "commentary": row["Commentary"]
            })

    return JsonResponse({
        "match_code": code,
        "commentary": commentary
    })

genai.configure(api_key=settings.GEMINI_API_KEY)


@api_view(['POST'])
def chat_with_gemini(request):
    user_input = request.data.get('message', '')
    if not user_input:
        return Response({"error": "Message is required"}, status=400)

    try:
        model = genai.GenerativeModel('models/gemini-2.0-flash')
        chat = model.start_chat(history=[])
        response = chat.send_message(user_input)
        return Response({"reply": response.text})
    except Exception as e:
        return Response({"error": str(e)}, status=500)
