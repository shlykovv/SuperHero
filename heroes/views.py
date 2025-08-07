import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from heroes.models import HeroModel
from heroes.serializers import HeroSerializer


class HeroAPIView(APIView):

    def get(self, request):
        queryset = HeroModel.objects.all()
        name = request.query_params.get('name')

        params = [
            ('intellegence', request.query_params.get('intellegence')),
            ('strength', request.query_params.get('strength')),
            ('speed', request.query_params.get('speed')),
            ('power', request.query_params.get('power'))]
        
        if name:
            queryset = queryset.filter(name__iexact=name)

        for field, value in params:
            if value:
                if value.startswith('>='):
                    queryset = queryset.filter(**{f'{field}__gte': int(value[2:])})
                elif value.startswith('<='):
                    queryset = queryset.filter(**{f'{field}__lte': int(value[2:])})
                else:
                    queryset = queryset.filter(**{f'{field}': int(value)})

        if not queryset.exists():
            return Response(
                {'error': 'No heroes found'},
                status=status.HTTP_404_NOT_FOUND )
        serializer = HeroSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        name = request.data.get('name')
        if not name:
            return Response(
                {'error': 'Name is required'},
                status=status.HTTP_400_BAD_REQUEST)
        if HeroModel.objects.filter(name=name).exists():
            return Response(
                {'detail': 'Hero already exists'},
                status=status.HTTP_200_OK
            )
        url = f'{settings.API_URL}/{settings.SECRET_API_TOKEN}/search/{name}/'
        try:
            response = requests.get(url)
            data = response.json()
        except Exception as ex:
            return Response(
                {'error': 'API request failed'},
                status=status.HTTP_502_BAD_GATEWAY)

        for result in data.get('results', []):
            if result['name'].lower() == name.lower():
                stats = result.get('powerstats', {})
                hero = HeroModel.objects.create(
                    name=result['name'],
                    intellegence=stats.get('intellegence', 0),
                    strength=stats.get('strength', 0),
                    speed=stats.get('speed', 0),
                    power=stats.get('power', 0)
                )
                return Response(
                    HeroSerializer(hero).data,
                    status=status.HTTP_201_CREATED)
        return Response(
            {'error': 'Exact hero not found'},
            status=status.HTTP_404_NOT_FOUND)
