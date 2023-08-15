from rest_framework import serializers
from content_manager_app.models import CodeWaveComment, CodeWaveJob, CodeWavePoll, CodeWavePollOption, CodeWaveStory

# Serializers for each model

class CodeWaveEditStorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(required=False)
    text = serializers.CharField(required=False)
    score = serializers.IntegerField(required=False)
    deleted = serializers.IntegerField(required=False)

class CodeWaveEditJobSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(required=False)
    text = serializers.CharField(required=False)
    score = serializers.IntegerField(required=False)
    deleted = serializers.IntegerField(required=False)

class CodeWaveEditCommentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.CharField(required=False)
    score = serializers.IntegerField(required=False)
    deleted = serializers.IntegerField(required=False)

class CodeWaveEditPollSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    score = serializers.IntegerField(required=False)
    deleted = serializers.IntegerField(required=False)

class CodeWaveEditPollOptionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    score = serializers.IntegerField(required=False)
    deleted = serializers.IntegerField(required=False)
    

# A dictionary for easy access to serializers based on the item_type
EDIT_SERIALIZER_MAP = {
    'story': CodeWaveEditStorySerializer,
    'job': CodeWaveEditJobSerializer,
    'comment': CodeWaveEditCommentSerializer,
    'poll': CodeWaveEditPollSerializer,
    'pollopt': CodeWaveEditPollOptionSerializer
}