from rest_framework.response import Response
from rest_framework.views import APIView
from core.selectors import benefits_inactivity_periods


class BenefitsInactivity(APIView):

    def get(self, request):
        venue = request.query_params.get("venueId")
        query = benefits_inactivity_periods(venue_id=venue, since=180)
        return Response(query)
