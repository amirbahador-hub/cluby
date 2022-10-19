from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from core.models import Benefit
from core.selectors import available_benefits
from rest_framework import status


class AvailableBenefits(APIView):
    class InputSerializer(serializers.Serializer):
        personId = serializers.IntegerField()
        venueId = serializers.IntegerField()
        timestamp = serializers.DateTimeField()

    class OutputSerializer(serializers.ModelSerializer):
        venueId = serializers.IntegerField(source="venueid_id")

        class Meta:

            model = Benefit
            fields = (
                "id",
                "title",
                "venueId",
                "recurrence",
            )

    def post(self, request):
        """
        ## valid request:
            {
                "personId": 1,
                "venueId": 1,
                "timestamp": "2022-09-25 04:49:06"
                }
        """
        serializer = self.InputSerializer(data=request.data)
        if serializer.is_valid():

            query = available_benefits(
                timestamp=serializer.validated_data["timestamp"],
                venue_id=serializer.validated_data["venueId"],
                person_id=serializer.validated_data["personId"],
            )

            serializer = self.OutputSerializer(query, many=True)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
