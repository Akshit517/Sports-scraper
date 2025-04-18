
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LiveCricketStatsView, get_commentary,chat_with_gemini
urlpatterns = [
    path('live-stats/', LiveCricketStatsView.as_view(), name='live-cricket-stats'),
    path("commentary/<str:code>/", get_commentary, name="get_commentary"),
path('chatbot/', chat_with_gemini, name='chat_with_gemini'),
]
