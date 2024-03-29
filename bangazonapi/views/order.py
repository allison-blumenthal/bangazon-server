from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import Order, User, PaymentType


class OrderView(ViewSet):
  """Bangazon API order view"""
  
  def retrieve(self, request, pk):
    """Handle GET requests for a single order
    
    Returns:
        Response -- JSON serialized order
    """
    try:
      order = Order.objects.get(pk=pk)
      
      serializer = OrderSerializer(order)
      return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Order.DoesNotExist as ex:
        return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
      
  def list(self, request):
    """Handle GET requests to get all orders
    
    Returns:
        Response -- JSON serialized list of all orders
    """
    
    orders = Order.objects.all()
    
    # define query params
    customer_id = request.query_params.get('customer_id', None)
    is_completed = request.query_params.get('is_completed')
    
    if customer_id is not None:
      try:
          # customer_id query param is converted to an integer
          customer_id = int(customer_id)
      except ValueError:
          return Response({'message': 'Invalid customer_id'}, status=status.HTTP_400_BAD_REQUEST)
        
      #filter orders by customer_id
      orders = orders.filter(customer_id=customer_id)
      
    if is_completed is not None:
      if is_completed.lower() in ['true', 'false']:
          is_completed = is_completed.lower() == 'true'
          orders = orders.filter(is_completed=is_completed)
      else:
          return Response({'message': 'Invalid is_completed value'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
  
  def create(self, request):
    """Handle POST operations for order
    
    Returns:
        Response -- JSON serialized order instance
    """
    
    customer_id = User.objects.get(pk=request.data["customerId"])
    payment_type = PaymentType.objects.get(pk=request.data["paymentType"])
    
    order = Order.objects.create(
      customer_id=customer_id,
      payment_type=payment_type,
      total=request.data["total"],
      needs_shipping=request.data["needsShipping"],
      is_completed=request.data["isCompleted"],
      date_placed=request.data["datePlaced"]
    )
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
    
  def update(self, request, pk):
    """Handle PUT requests for an order
    
    Returns:
        Response -- Empty body with 204 status code
    """
    
    order = Order.objects.get(pk=pk)
    order.total = request.data["total"]
    order.needs_shipping=request.data["needsShipping"]
    order.is_completed=request.data["isCompleted"]
    order.date_placed=request.data["datePlaced"]
    
    customer_id = User.objects.get(pk=request.data["customerId"])
    order.customer_id = customer_id
    
    payment_type = PaymentType.objects.get(pk=request.data["paymentType"])
    order.payment_type = payment_type
    
    order.save()
    
    return Response(None, status=status.HTTP_204_NO_CONTENT)


class OrderSerializer(serializers.ModelSerializer):
  """JSON serializer for orders"""
  
  class Meta:
      model = Order
      fields = ('id', 'customer_id', 'payment_type', 'total', 'needs_shipping', 'is_completed', 'date_placed')
      depth = 1
