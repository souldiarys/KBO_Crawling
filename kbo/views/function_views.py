from django.db.models import Q
from django.http.response import HttpResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

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

# /hitter/
@api_view(['GET'])
def hitter_all(request):
    if request.method == 'GET': # List All hitter's all season record
        hitters = Hitter.objects.all()
        serializer = HitterSerializer(hitters, many=True)
        return Response(serializer.data)

# /pitcher/
@api_view(['GET'])
def pitcher_all(request):
    if request.method == 'GET': # List All pitcher's all season record
        pitchers = Pitcher.objects.all()
        serializer = PitcherSerializer(pitchers, many=True)
        return Response(serializer.data)

# /hitter/<int:player_id>/
@api_view(['GET', 'DELETE'])
def hitter_id(request, player_id):
    try:
        hitters = Hitter.objects.filter(player_id=player_id).all()
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET': # Retrieve a hitter's all season record
        serializer = HitterSerializer(hitters, many=True)
        return Response(serializer.data)
    elif request.method == 'DELETE': # Delete a hitter's all season record
        hitters.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# /pitcher/<int:player_id>/
@api_view(['GET', 'DELETE'])
def pitcher_id(request, player_id):
    try:
        pitchers = Pitcher.objects.filter(player_id=player_id).all()
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET': # Retrieve a pitcher's all season record
        serializer = PitcherSerializer(pitchers, many=True)
        return Response(serializer.data)
    elif request.method == 'DELETE': # Delete a pitcher's all season record
        pitchers.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# /year/<int:year>/hitter/
@api_view(['GET'])
def hitter_year_all(request, year):
    try:
        hitters = Hitter.objects.filter(year=year).all()
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET': # List All hitter's all season record
        serializer = HitterSerializer(hitters, many=True)
        return Response(serializer.data)

# /year/<int:year>/pitcher/
@api_view(['GET'])
def pitcher_year_all(request, year):
    try:
        pitchers = Pitcher.objects.filter(year=year).all()
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET': # List All pitcher's all season record
        serializer = PitcherSerializer(pitchers, many=True)
        return Response(serializer.data)

# /year/<int:year>/hitter/<int:player_id>/
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def hitter_year_id(request, year, player_id):
    try:
        hitter = Hitter.objects.filter(Q(player_id=player_id) & Q(year=year)).get()
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = HitterSerializer(hitter)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = HitterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        serializer = HitterSerializer(hitter, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        hitter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# /year/<int:year>/pitcher/<int:player_id>/
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def pitcher_year_id(request, year, player_id):
    try:
        pitcher = Pitcher.objects.filter(Q(player_id=player_id) & Q(year=year)).get()
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PitcherSerializer(pitcher)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PitcherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        serializer = PitcherSerializer(pitcher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        pitcher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# /team/<int:team_id>/hitter/
@api_view(['GET'])
def team_hitter_all(request, team_id):
    try:
        hitter = Hitter.objects.filter(team_id=team_id).all()
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = HitterSerializer(hitter, many=True)
        return Response(serializer.data)

# /team/<int:team_id>/pitcher/
@api_view(['GET'])
def team_pitcher_all(request, team_id):
    try:
        pitcher = Pitcher.objects.filter(team_id=team_id).all()
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PitcherSerializer(pitcher, many=True)
        return Response(serializer.data)

# /year/<int:year>/team/<int:team_id>/hitter/
@api_view(['GET'])
def team_hitter_year(request, year, team_id):
    try:
        hitter = Hitter.objects.filter(Q(team_id=team_id) & Q(year=year)).all()
    except:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = HitterSerializer(hitter, many=True)
        return Response(serializer.data)

# /year/<int:year>/team/<int:team_id>/pitcher/
@api_view(['GET'])
def team_pitcher_year(request, year, team_id):
    try:
        pitcher = Pitcher.objects.filter(Q(team_id=team_id) & Q(year=year)).all()
    except:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PitcherSerializer(pitcher, many=True)
        return Response(serializer.data)