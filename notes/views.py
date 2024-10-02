from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from notes.models import User,Task

from notes.serializers import UserSerializer,TaskSerializer

from rest_framework.response import Response

from rest_framework import authentication,permissions

from notes.permissions import OwnerOnly

from rest_framework.views import APIView

from django.db.models import Count

class UserCreationView(generics.CreateAPIView):
    
    serializer_class=UserSerializer
    
    
    # def post(self,request,*args, **kwargs):
        
        # serializer_instance=UserSerializer(data=request.data)
        
        # if serializer_instance.is_valid():
            
        #     data=serializer_instance.validated_data
            
        #     User.objects.create_user(**data)
            
        #     return Response(data=serializer_instance.data)
        
        # return Response(data=serializer_instance.errors)
            
class TaskListCreateView(generics.ListCreateAPIView):
    
    # authentication_classes=[authentication.BasicAuthentication]
    
    authentication_classes=[authentication.TokenAuthentication]
    
    permission_classes=[permissions.IsAuthenticated]
    
    serializer_class=TaskSerializer
    
    queryset=Task.objects.all()
    
    
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        
        qs=Task.objects.filter(owner=self.request.user)
        
        if "category" in self.request.query_params:
            
            category_value=self.request.query_params.get("category")
            
            qs=qs.filter(category=category_value)
            
        if "priority" in self.request.query_params:
            
            priority_value=self.request.query_params.get("priority")
            
            qs=qs.filter(priority=priority_value)
        
        return qs
    
    
class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    
    serializer_class=TaskSerializer
    
    queryset=Task.objects.all()
    
    # authentication_classes=[authentication.BasicAuthentication]

    authentication_classes=[authentication.TokenAuthentication]
    
    permission_classes=[OwnerOnly]
    
    
class TaskSummaryView(APIView):
    
    # authentication_classes=[authentication.BasicAuthentication]
    
    authentication_classes=[authentication.TokenAuthentication]
    
    permission_classes=[permissions.IsAuthenticated]
    
    def get(self,request,*args, **kwargs):
        
        qs=Task.objects.filter(owner=request.user)
        
        category_summary=qs.values("category").annotate(count=Count("category"))
        
        priority_summary=qs.values("priority").annotate(count=Count("priority"))

        status_summary=qs.values("status").annotate(count=Count("status"))
        
        task_count=qs.count()
        
        context={
            "category_summary":category_summary,
            
            "status_summary":status_summary,
            
            "priority_summary":priority_summary,
            
            "total_count":task_count
        }
        
        return Response(data=context)
    
    
class CategorieListView(APIView):
    
    def get(self,request,*args, **kwargs):
        
        qs=Task.category_choices
        
        st={cat for tp in qs for cat in tp}
        
        return Response(data=st)