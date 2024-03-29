"""View module for handling requests about song genres"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import PaymentType


class PaymentTypeView(ViewSet):
    """Bangazon API payment_type view"""
    
    def retrieve(self, request, pk):
      """Handle GET requests for a single payment_type
      
      Returns:
          Response -- JSON serialized payment_type
      """
      
      try:
          payment_type = PaymentType.objects.get(pk=pk)
          
          serializer = PaymentTypeSerializer(payment_type)
          return Response(serializer.data, status=status.HTTP_200_OK)
        
      except PaymentType.DoesNotExist as ex:
          return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
      """Handle GET requests to get all payment_types
      
      Returns:
          Response -- JSON serialized list of all payment_types
      """
      
      payment_types = PaymentType.objects.all()
      
      serializer = PaymentTypeSerializer(payment_types, many=True)
      return Response(serializer.data)
    
    def create(self, request):
      """Handle POST operations for payment_type
      
      Returns:
          Response -- JSON serialized payment_type instance
      """
      
      payment_type = PaymentType.objects.create(
        label=request.data["label"]
      )
      serializer = PaymentTypeSerializer(payment_type)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
      """Handle PUT requests for a payment_type
      
      Returns:
          Response -- Empty body with 204 status code
      """
      payment_type = PaymentType.objects.get(pk=pk)
      payment_type.label = request.data["label"]
      
      payment_type.save()
      
      return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
      payment_type = PaymentType.objects.get(pk=pk)
      payment_type.delete()
      return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class PaymentTypeSerializer(serializers.ModelSerializer):
  """JSON serializer for categories"""
  
  class Meta:
      model = PaymentType
      fields = ('id', 'label')
      depth = 0
