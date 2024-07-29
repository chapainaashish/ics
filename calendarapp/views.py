import io

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .parser import parse_icalendar  # Make sure this import is correct


class ICSFileUploadView(APIView):
    def post(self, request):
        ics_file = request.FILES.get("file")
        if not ics_file:
            return Response(
                {"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Read file content into memory
        file_content = ics_file.read()
        file_like_object = io.BytesIO(file_content)

        # Parse calendar
        try:
            events = parse_icalendar(file_like_object)
            return Response(events, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
