from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Visitor
from .serializers import VisitorSerializer
from rest_framework.response import Response
from rest_framework.decorators import action


# Create your views here.
class VisitorViewSet(viewsets.ModelViewSet):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) #validate the data
        self.perform_create(serializer) #save the new visitor
        headers = self.get_success_headers(serializer.data)

        #Custom response with status code and success message
        return Response({
            'message': 'Visitor added successfully',
            'data': serializer.data
        },status=status.HTTP_201_CREATED, headers=headers)
    

    #update member record
    def udpate(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)

        #Return custom response with success message
        return Response({
            'message': 'Visitor updated successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK, headers=headers)
    

    
    #delete member record
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        #Custom response with sucess message
        return Response({
            'message': 'Visitor deleted successfully',
        
        }, status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        queryset =  super().get_queryset()
        gender = self.request.query_params.get('gender', None)
        if gender:
            queryset = queryset.filter(gender=gender)
        return queryset
    

    @action(detail=False, methods=['get'])
    def males(self):
        queryset = self.get_queryset().filter(gender='male')
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

    @action(detail=False, methods=['get'])
    def males(self):
        queryset = self.get_queryset().filter(gender='female')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    