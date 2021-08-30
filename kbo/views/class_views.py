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
    def get(self, request, format=None):
        hitters = Hitter.objects.all()
        serializer = HitterSerializer(hitters, many=True)
        return Response(serializer.data)

class pitcher_all(APIView):
    def get(self, request, format=None):
        pitchers = Pitcher.objects.all()
        serializer = PitcherSerializer(pitchers, many=True)
        return Response(serializer.data)

class hitter_id(APIView):
    def get_object(self, player_id):
        try:
            return Hitter.objects.filter(player_id=player_id).all()
        except:
            raise Http404

    def get(self, request, player_id, format=None):
        hitters = self.get_object(player_id)
        serializer = HitterSerializer(hitters, many=True)
        return Response(serializer.data)

    def delete(self, request, player_id, formant=None):
        hitters = self.get_object(player_id)
        hitters.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class pitcher_id(APIView):
    def get_object(self, player_id):
        try:
            return Pitcher.objects.filter(player_id=player_id).all()
        except:
            raise Http404

    def get(self, request, player_id, format=None):
        pitchers = self.get_object(player_id)
        serializer = PitcherSerializer(pitchers, many=True)
        return Response(serializer.data)

    def delete(self, request, player_id, formant=None):
        pitchers = self.get_object(player_id)
        pitchers.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class hitter_year_all(APIView):
    def get_object(self, year):
        try:
            return Hitter.objects.filter(year=year).all()
        except:
            raise Http404

    def get(self, request, year, format=None):
        hitters = self.get_object(year)
        serializer = HitterSerializer(hitters, many=True)
        return Response(serializer.data)

class pitcher_year_all(APIView):
    def get_object(self, year):
        try:
            return Pitcher.objects.filter(year=year).all()
        except:
            raise Http404

    def get(self, request, year, format=None):
        pitchers = self.get_object(year)
        serializer = PitcherSerializer(pitchers, many=True)
        return Response(serializer.data)

class hitter_year_id(APIView):
    def get_object(self, year, player_id):
        try:
            return Hitter.objects.filter(Q(player_id=player_id) & Q(year=year)).get()
        except:
            raise Http404
    
    def get(self, request, year, player_id, format=None):
        hitter = self.get_object(year, player_id)
        serializer = HitterSerializer(hitter)
        return Response(serializer.data)

    def post(self, request, year, player_id, format=None):
        serializer = HitterSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, year, player_id, format=None):
        hitter = self.get_object(year, player_id)
        serializer = HitterSerializer(hitter, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, year, player_id, format=None):
        hitter = self.get_object(year, player_id)
        hitter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class pitcher_year_id(APIView):
    def get_object(self, year, player_id):
        try:
            return Pitcher.objects.filter(Q(player_id=player_id) & Q(year=year)).get()
        except:
            raise Http404
    
    def get(self, request, year, player_id, format=None):
        pitcher = self.get_object(year, player_id)
        serializer = PitcherSerializer(pitcher)
        return Response(serializer.data)

    def post(self, request, year, player_id, format=None):
        serializer = PitcherSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, year, player_id, format=None):
        pitcher = self.get_object(year, player_id)
        serializer = PitcherSerializer(pitcher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, year, player_id, format=None):
        pitcher = self.get_object(year, player_id)
        pitcher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class team_hitter_all(APIView):
    def get_object(self, team_id):
        try:
            return Hitter.objects.filter(team_id=team_id).all()
        except:
            raise Http404

    def get(self, request, team_id, format=None):
        hitters = self.get_object(team_id)
        serializer = HitterSerializer(hitters, many=True)
        return Response(serializer.data)

class team_pitcher_all(APIView):
    def get_object(self, team_id):
        try:
            return Pitcher.objects.filter(team_id=team_id).all()
        except:
            raise Http404

    def get(self, request, team_id, format=None):
        pitchers = self.get_object(team_id)
        serializer = PitcherSerializer(pitchers, many=True)
        return Response(serializer.data)

class team_hitter_year(APIView):
    def get_object(self, year, team_id):
        try:
            return Hitter.objects.filter(Q(team_id=team_id) & Q(year=year)).all()
        except:
            raise Http404

    def get(self, request, year, team_id, format=None):
        hitters = self.get_object(year, team_id)
        serializer = HitterSerializer(hitters, many=True)
        return Response(serializer.data)

class team_pitcher_year(APIView):
    def get_object(self, year, team_id):
        try:
            return Pitcher.objects.filter(Q(team_id=team_id) & Q(year=year)).all()
        except:
            raise Http404

    def get(self, request, year, team_id, format=None):
        pitchers = self.get_object(year, team_id)
        serializer = PitcherSerializer(pitchers, many=True)
        return Response(serializer.data)