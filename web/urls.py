from django.urls import path
from .views import IndexView, StartRecordingView, StopRecordingView, VideoFeedView ,VideoRecordingPageView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('start_recording/', StartRecordingView.as_view(), name='start_recording'),
    path('stop_recording/', StopRecordingView.as_view(), name='stop_recording'),
    path('video_feed/', VideoFeedView.as_view(), name='video_feed'),
    path('video_recording/',VideoRecordingPageView.as_view(),name="video_recording")
]