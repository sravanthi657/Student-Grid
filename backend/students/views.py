from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import Student
from .serializers import StudentSerializer

@api_view(['GET'])
def student_list(request):
    try:
        # Get pagination parameters from query parameters
        page_number = request.query_params.get('page', 1)
        page_size = request.query_params.get('page_size', 10)

        # Retrieve all students queryset
        students = Student.objects.all()

        # Apply filtering based on query parameters
        name = request.query_params.get('name', None)
        if name:
            students = students.filter(name__icontains=name)

        total_marks_min = request.query_params.get('total_marks_min', None)
        if total_marks_min:
            students = students.filter(total_marks__gte=int(total_marks_min))

        total_marks_max = request.query_params.get('total_marks_max', None)
        if total_marks_max:
            students = students.filter(total_marks__lte=int(total_marks_max))

        # Paginate the queryset
        paginator = PageNumberPagination()
        paginator.page_size = page_size
        paginated_students = paginator.paginate_queryset(students, request)

        # Serialize paginated data
        serializer = StudentSerializer(paginated_students, many=True)

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
