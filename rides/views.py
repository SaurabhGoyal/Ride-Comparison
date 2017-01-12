from rest_framework import (
    generics as rest_generics,
    response as rest_response,
    status as rest_status,
)

from rides import (
    serializers as rides_serializers,
    utils as rides_utils,
)


class RideEstimateView(rest_generics.ListAPIView):
    """
    API to view a list of available rides along-with estimates.
    """

    def list(self, request, *args, **kwargs):
        serializer = rides_serializers.RideEstimateParamsSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        params = serializer.data
        order_by = params.pop(u'order_by', None)
        uber_data = rides_utils.get_uber_data(**params)
        ola_data = rides_utils.get_ola_data(**params)
        final_rides_data = rides_utils.combine_rides_data(uber_data, ola_data)
        if order_by:
            key = {
                1: lambda x: x[u'data'][u'eta'],
                2: lambda x: -x[u'data'][u'low_estimate'],
                3: lambda x: -x[u'data'][u'high_estimate'],
            }
            final_rides_data = sorted(final_rides_data, key=key[order_by])
        return rest_response.Response(data=final_rides_data, status=rest_status.HTTP_200_OK)
