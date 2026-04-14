from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
class SummarizeFindingsView(APIView):

    def post(self, request):
        findings = request.data.get('findings')
        if not findings:
            return Response({"error": "Findings are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Here you would implement the logic to summarize the findings
        # For demonstration purposes, we'll just return a dummy summary
        summary = f"Summary of findings: {findings[:50]}..."  # Dummy summary
        
        return Response({"summary": summary}, status=status.HTTP_200_OK)