"""View module for handling requests about song genres"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import Category


class CategoryView(ViewSet):
    """Bangazon API catgory view"""
    
    def retrieve(self, request, pk):
      """Handle GET requests for a single category
      
      Returns:
          Response -- JSON serialized category
      """
      
      try:
          category = Category.objects.get(pk=pk)
          
          serializer = CategorySerializer(category)
          return Response(serializer.data, status=status.HTTP_200_OK)
        
      except Category.DoesNotExist as ex:
          return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
      """Handle GET requests to get all categories
      
      Returns:
          Response -- JSON serialized list of all categories
      """
      
      categories = Category.objects.all()
      
      serializer = CategorySerializer(categories, many=True)
      return Response(serializer.data)
    
class CategorySerializer(serializers.ModelSerializer):
  """JSON serializer for categories"""
  
  class Meta:
      model = Category
      fields = ('id', 'label')
      depth = 0
