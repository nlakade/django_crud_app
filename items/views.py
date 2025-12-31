from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from django.db.models import Count, Sum
from datetime import datetime, timedelta
import requests
from .models import Item
from .serializers import ItemSerializer
from django.conf import settings

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get count of items by category"""
        category_stats = Item.objects.values('category').annotate(
            total=Count('id'),
            total_value=Sum('price')
        )
        return Response(category_stats)
    
    @action(detail=False, methods=['get'])
    def recent_items(self, request):
        """Get items created in the last 7 days"""
        seven_days_ago = datetime.now() - timedelta(days=7)
        recent_items = Item.objects.filter(created_at__gte=seven_days_ago)
        serializer = self.get_serializer(recent_items, many=True)
        return Response(serializer.data)

class WeatherAPIView(APIView):
    """Third-party API integration example: OpenWeather API"""
    
    def get(self, request):
        city = request.query_params.get('city', 'London')
        
        # Using OpenWeather API (you need to sign up for free API key)
        api_key = settings.OPENWEATHER_API_KEY
        if not api_key:
            return Response({'error': 'OpenWeather API key not configured'}, 
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        try:
            # First, get coordinates for the city
            geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
            geo_response = requests.get(geo_url, timeout=10)
            geo_data = geo_response.json()
            
            if not geo_data:
                return Response({'error': 'City not found'}, status=status.HTTP_404_NOT_FOUND)
            
            lat = geo_data[0]['lat']
            lon = geo_data[0]['lon']
            
            # Get weather data
            weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
            weather_response = requests.get(weather_url, timeout=10)
            weather_data = weather_response.json()
            
            return Response({
                'city': city,
                'temperature': weather_data['main']['temp'],
                'description': weather_data['weather'][0]['description'],
                'humidity': weather_data['main']['humidity'],
                'wind_speed': weather_data['wind']['speed']
            })
            
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DashboardView(APIView):
    """Dashboard with data visualization"""
    
    def get(self, request):
        # Get statistics for visualization
        category_stats = Item.objects.values('category').annotate(
            count=Count('id'),
            total_value=Sum('price')
        )
        
        # Get daily item counts for the last 7 days
        seven_days_ago = datetime.now() - timedelta(days=7)
        daily_counts = Item.objects.filter(
            created_at__gte=seven_days_ago
        ).extra({
            'date': "date(created_at)"
        }).values('date').annotate(count=Count('id')).order_by('date')
        
        # Prepare data for Chart.js
        categories = [stat['category'] for stat in category_stats]
        category_counts = [stat['count'] for stat in category_stats]
        category_values = [float(stat['total_value'] or 0) for stat in category_stats]
        
        dates = [stat['date'].strftime('%Y-%m-%d') for stat in daily_counts]
        daily_counts_data = [stat['count'] for stat in daily_counts]
        
        # Total statistics
        total_items = Item.objects.count()
        total_value = Item.objects.aggregate(total=Sum('price'))['total'] or 0
        avg_price = Item.objects.aggregate(avg=Sum('price')/Count('id'))['avg'] or 0
        
        context = {
            'categories': categories,
            'category_counts': category_counts,
            'category_values': category_values,
            'dates': dates,
            'daily_counts': daily_counts_data,
            'total_items': total_items,
            'total_value': float(total_value),
            'avg_price': float(avg_price),
        }
        
        return render(request, 'items/dashboard.html', context)

def items_list_view(request):
    """HTML view for browsing items"""
    items = Item.objects.all()
    return render(request, 'items/items_list.html', {'items': items})