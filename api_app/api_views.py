from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from content_manager_app.models import CodeWaveComment, CodeWaveJob, CodeWavePoll, CodeWavePollOption, CodeWaveStory

from api_app.serializers import EDIT_SERIALIZER_MAP


class UpdateItemView(APIView):
    def post(self, request):
        # Get item_type from the request data
        item_type = request.data.get('type')
        
        # Check if the item_type is valid
        if item_type not in EDIT_SERIALIZER_MAP:
            return Response({"error": "Invalid item_type provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get the appropriate serializer
        SerializerClass = EDIT_SERIALIZER_MAP[item_type]
        serializer = SerializerClass(data=request.data)
        
        # Validate data
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Fetch the object based on item_id and update it
        item_id = serializer.validated_data['id']
        
        MODEL_MAP = {
            'story': CodeWaveStory,
            'job': CodeWaveJob,
            'comment': CodeWaveComment,
            'poll': CodeWavePoll,
            'pollopt': CodeWavePollOption
        }
        
        item = get_object_or_404(MODEL_MAP[item_type], item_id=item_id)
        
        for field, value in serializer.validated_data.items():
            setattr(item, field, value)
        
        item.save()
        
        return Response({"success": "Item updated successfully."}, status=status.HTTP_200_OK)
