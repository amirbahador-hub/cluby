from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from core.models import Benefit, Venue
from core.selectors.populars import popular_benefits
from core.selectors.inactives import benefits_inactivity_periods
from core.selectors.availables import available_benefits
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class BenefitsInactivity(APIView):

    def get(self, request):
        venue = request.query_params.get("venueId")
        query = benefits_inactivity_periods(venue_id=venue, since=180)
        return Response(query)


class PopularBenefits(APIView):

    class BenefitSerializer(serializers.ModelSerializer):
        benefitId = serializers.IntegerField(source="id")
        usageCount = serializers.SerializerMethodField("get_usageCount")

        class Meta:
            model = Benefit
            fields = ("benefitId", "usageCount")

        def get_usageCount(self, obj):
            return obj.usageCount

    class OutputSerializer(serializers.ModelSerializer):

        venueId = serializers.IntegerField(source="id")
        topBenefits180Days = serializers.SerializerMethodField("get_top_benefits")

        class Meta:
            model = Venue
            fields = (
                "venueId",
                "topBenefits180Days",
            )

        def get_top_benefits(self, venue):
            query = venue.benefit_set.all()[:3]
            return PopularBenefits.BenefitSerializer(
                instance=query, many=True, context=self.context
            ).data

    def get(self, request):
        query = popular_benefits(since=180)
        serializer = self.OutputSerializer(query, many=True)
        return Response(serializer.data)


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

    @swagger_auto_schema(request_body=InputSerializer)
    def post(self, request):
        """
        return available benefits 
        
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
