from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer
from .serializers import CustomerSerializer

class CustomerList(APIView):
    
    def get(self,request):
        customer = Customer.objects.all()
        serializer = CustomerSerializer(customer,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request):
        is_many = isinstance(request.data, list)

        serializer = CustomerSerializer(data = request.data,many = is_many)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
class CustomerDetail(APIView):
    def get(self,request,pk):
        try:
            customer = Customer.objects.get(pk=pk)
            serializer = CustomerSerializer(customer)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({'error':'Customer not found'},status=status.HTTP_404_NOT_FOUND)
    def put(self,request,pk):
        try:
            customer = Customer.objects.get(pk=pk)
            serializer = CustomerSerializer(customer,data=request.data)
        except Customer.DoesNotExist:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)   
    def delete(self,request,id):
        try:    
            customer = Customer.objects.get(pk=id)
            customer.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)  
        except Customer.DoesNotExist:
            return Response({'error':'Customer not found'},status=status.HTTP_404_NOT_FOUND)


