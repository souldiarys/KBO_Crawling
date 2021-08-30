from django.db.models import Q
from django.http.response import Http404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Hitter, Pitcher
from ..serializers import HitterSerializer, PitcherSerializer

# All Season
# /hitter/
# /pitcher/
# /hitter/<int:player_id>/
# /pitcher/<int:player_id>/
# /team/<int:team_id>/hitter/
# /team/<int:team_id>/pitcher/

# A Specific Season
# /year/<int:year>/hitter/
# /year/<int:year>/pitcher/
# /year/<int:year>/hitter/<int:player_id>/
# /year/<int:year>/pitcher/<int:player_id>/
# /year/<int:year>/team/<int:team_id>/hitter/
# /year/<int:year>/team/<int:team_id>/pitcher/

class hitter_all(APIView):
    def get(self, request, *args, **kwargs):
        hitters = Hitter.objects.all()
        serializer = HitterSerializer(hitters, many=True)
        return Response(serializer.data)

class pitcher_all(APIView):
    def get(self, request, *args, **kwargs):
        pitchers = Pitcher.objects.all()
        serializer = PitcherSerializer(pitchers, many=True)
        return Response(serializer.data)

class hitter_id(APIView):
    def get_object(self):
        try:
            return Hitter.objects.filter(player_id=self.kwargs['player_id']).all()
        except:
            raise Http404

    def get(self, request, *args, **kwargs):
        hitters = self.get_object()
        serializer = HitterSerializer(hitters, many=True)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        hitters = self.get_object()
        hitters.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class pitcher_id(APIView):
    def get_object(self):
        try:
            return Pitcher.objects.filter(player_id=self.kwargs['player_id']).all()
        except:
            raise Http404

    def get(self, request, *args, **kwargs):
        pitchers = self.get_object()
        serializer = PitcherSerializer(pitchers, many=True)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        pitchers = self.get_object()
        pitchers.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class hitter_year_all(APIView):
    def get_object(self):
        try:
            return Hitter.objects.filter(year=self.kwargs['year']).all()
        except:
            raise Http404

    def get(self, request, *args, **kwargs):
        hitters = self.get_object()
        serializer = HitterSerializer(hitters, many=True)
        return Response(serializer.data)

class pitcher_year_all(APIView):
    def get_object(self):
        try:
            return Pitcher.objects.filter(year=self.kwargs['year']).all()
        except:
            raise Http404

    def get(self, request, *args, **kwargs):
        pitchers = self.get_object()
        serializer = PitcherSerializer(pitchers, many=True)
        return Response(serializer.data)

class hitter_year_id(APIView):
    def get_object(self):
        try:
            return Hitter.objects.filter(Q(player_id=self.kwargs['player_id']) & Q(year=self.kwargs['year'])).get()
        except:
            raise Http404
    
    def get(self, request, *args, **kwargs):
        hitter = self.get_object()
        serializer = HitterSerializer(hitter)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = HitterSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, *args, **kwargs):
        hitter = self.get_object()
        serializer = HitterSerializer(hitter, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        hitter = self.get_object()
        hitter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class pitcher_year_id(APIView):
    def get_object(self):
        try:
            return Pitcher.objects.filter(Q(player_id=self.kwargs['player_id']) & Q(year=self.kwargs['year'])).get()
        except:
            raise Http404
    
    def get(self, request, *args, **kwargs):
        pitcher = self.get_object()
        serializer = PitcherSerializer(pitcher)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = PitcherSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, *args, **kwargs):
        pitcher = self.get_object()
        serializer = PitcherSerializer(pitcher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pitcher = self.get_object()
        pitcher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class team_hitter_all(APIView):
    def get_object(self):
        try:
            return Hitter.objects.filter(team_id=self.kwargs['team_id']).all()
        except:
            raise Http404

    def get(self, request, *args, **kwargs):
        hitters = self.get_object()
        serializer = HitterSerializer(hitters, many=True)
        return Response(serializer.data)

class team_pitcher_all(APIView):
    def get_object(self):
        try:
            return Pitcher.objects.filter(team_id=self.kwargs['team_id']).all()
        except:
            raise Http404

    def get(self, request, *args, **kwargs):
        pitchers = self.get_object()
        serializer = PitcherSerializer(pitchers, many=True)
        return Response(serializer.data)

class team_hitter_year(APIView):
    def get_object(self):
        try:
            return Hitter.objects.filter(Q(team_id=self.kwargs['team_id']) & Q(year=self.kwargs['year'])).all()
        except:
            raise Http404

    def get(self, request, *args, **kwargs):
        hitters = self.get_object()
        serializer = HitterSerializer(hitters, many=True)
        return Response(serializer.data)

class team_pitcher_year(APIView):
    def get_object(self):
        try:
            return Pitcher.objects.filter(Q(team_id=self.kwargs['team_id']) & Q(year=self.kwargs['year'])).all()
        except:
            raise Http404

    def get(self, request, *args, **kwargs):
        pitchers = self.get_object()
        serializer = PitcherSerializer(pitchers, many=True)
        return Response(serializer.data)