from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from core.models import Benefit, Venue
from core.selectors import popular_benefits
from django.db.models import Prefetch, Count, Q
from django.utils.timezone import now
from datetime import timedelta


class BenefitSerializer(serializers.ModelSerializer):
        benefitId = serializers.IntegerField(source='id')
        usageCount = serializers.SerializerMethodField('get_usageCount')

        class Meta:
            model = Benefit
            fields = (
                'benefitId',
                'usageCount'
            )

        def get_usageCount(self, obj):
            return obj.usageCount

class TestCore(APIView):


    class OutputSerializer(serializers.ModelSerializer):
        venueId = serializers.IntegerField(source='id')
        topBenefits180Days = serializers.SerializerMethodField('get_top_benefits')


        class Meta:
            model = Venue
            fields = (
                'venueId',
                'topBenefits180Days',
            )
            
        def get_top_benefits(self, obj):
            query = popular_benefits(venue=obj, limit=3, since=180)
            return BenefitSerializer(instance=query, many=True, context=self.context).data


    def get(self, request, *args, **kwargs):
        query = Venue.objects.prefetch_related(
                Prefetch('benefit_set',
                         queryset=Benefit.objects.annotate(
                             usageCount=Count("benefitusage", filter=Q(benefitusage__usagetimestamp__lt=now()-timedelta(days=180))),
                             ).order_by("-usageCount")
                         ),
                ).all()
        serializer = self.OutputSerializer(query, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        return Response(request.data)
