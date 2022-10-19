from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from core.models import Benefit, Venue
from core.selectors import popular_benefits


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
