from rest_framework import (
    serializers as rest_serializers,
)


class RideEstimateParamsSerializer(rest_serializers.Serializer):
    """
    Serializer to validate request parameters for ride-estimate view.
    """

    start_lat = rest_serializers.FloatField(min_value=-90, max_value=90, required=True)
    start_long = rest_serializers.FloatField(min_value=-180, max_value=180, required=True)
    end_lat = rest_serializers.FloatField(min_value=-90, max_value=90, required=True)
    end_long = rest_serializers.FloatField(min_value=-180, max_value=180, required=True)
