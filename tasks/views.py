from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Task
from .serializer import TaskSerializer
from rest_framework.decorators import api_view

class TaskListCreateView(APIView):
    def get(self, request):
        db = Task.objects.all()
        data = TaskSerializer(db, many=True)
        return Response(data.data)
    
    def post(self, request):
        tasks = TaskSerializer(data=request.data)
        if tasks.is_valid():
            tasks.save()
            return Response(data = {
                'message' : 'Your task is saved'
            },status=200)
        return Response(data = {
            'message' : 'Bad request'
        }, status=400)
    
class TaskDetailView(APIView):
    def get(self, request, pk):
        task = Task.objects.filter(id=pk).first()
        if not task:
            return Response(data= {
                'message' : 'Task not found'
            }, status = 404)
        db = TaskSerializer(task)
        return Response(db.data, status = 200)
        
    def put(self, request, pk):
        task = Task.objects.filter(id=pk).first()
        if not task:
            return Response(data = {
                'message' : 'Task not found'
            }, status = 404)
        db = TaskSerializer(task, data=request.data, partial=True)
        if db.is_valid():
            db.save()
            return Response(db.data, status = 200)
        return Response(status = 400)
        
    def delete(self, request, pk):
        task = Task.objects.filter(id=pk).first()
        if not task:
            return Response(data = {
                'error' : 'Task not found'
            }, status = 404)
        task.delete()
        return Response(data = {
            'message' : 'Task deleted successfully'
        },status = 200)
    

@api_view(['POST'])
def mark_completed(request, pk):
    task = Task.objects.filter(id=pk).first()
    if not task:
        return Response(data={
            'error' : 'Task not found'
        }, status = 404)
    task.is_completed = True
    task.save()
    db = TaskSerializer(task)
    return Response(db.data, status = 200)

@api_view(['POST'])
def mark_important(request, pk):
    task = Task.objects.filter(id=pk).first()
    if not task:
        return Response(data={
            'error' : 'Task not found'
        }, status=404)
    task.is_important = True
    task.save()
    db = TaskSerializer(task)
    return Response(db.data, status=200)
