from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TextAnalyzeSerializer, URLAnalyzeSerializer, ScanSerializer
from .services import analyze_and_save
from .models import Scan


def api_result(result):
    result.pop("scan", None)
    result.pop("normalized_input", None)
    result.pop("features", None)
    return result


class AnalyzeTextAPI(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = TextAnalyzeSerializer(data=request.data); serializer.is_valid(raise_exception=True)
        return Response(api_result(analyze_and_save(request.user, "TEXT", serializer.validated_data["text"])), status=status.HTTP_200_OK)


class AnalyzeURLAPI(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = URLAnalyzeSerializer(data=request.data); serializer.is_valid(raise_exception=True)
        return Response(api_result(analyze_and_save(request.user, "URL", serializer.validated_data["url"])), status=status.HTTP_200_OK)


class ScanListAPI(generics.ListAPIView):
    serializer_class = ScanSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self): return Scan.objects.filter(user=self.request.user).prefetch_related("signals")


class ScanDetailAPI(generics.RetrieveDestroyAPIView):
    serializer_class = ScanSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self): return Scan.objects.filter(user=self.request.user).prefetch_related("signals")
