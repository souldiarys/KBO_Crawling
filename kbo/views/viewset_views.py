from ..models import Hitter, Pitcher, Team
from ..serializers import HitterSerializer, PitcherSerializer, TeamSerializer

from rest_framework import viewsets, status
from rest_framework.response import Response

class KBOHitterViewSet(viewsets.ViewSet):
    def list(self, request):
        hitters = Hitter.objects.all()
        serializer = HitterSerializer(hitters, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = HitterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        hitters = Hitter.objects.all().filter(player_id = pk)
        serializer = HitterSerializer(hitters, many=True)
        return Response(serializer.data)

class KBOPitcherViewSet(viewsets.ViewSet):
    def list(self, request):
        pitchers = Pitcher.objects.all()
        serializer = PitcherSerializer(pitchers, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = PitcherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        pitchers = Pitcher.objects.all().filter(player_id = pk)
        serializer = PitcherSerializer(pitchers, many=True)
        return Response(serializer.data)

class KBOTeamViewSet(viewsets.ViewSet):
    def list(self, request):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        teams = Team.objects.all().filter(id = pk)
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)