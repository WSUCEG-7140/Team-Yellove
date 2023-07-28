# Import necessary modules
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
#for rest_framework: https://www.django-rest-framework.org/

# ISSUE 16 Implement user registration functionality

# API view for user registration
@api_view(['POST'])
@permission_classes([])
def create_user(request):
    # Create a serializer instance with the request data
    serializer = UserSerializer(data=request.data)
    
    # Check if the serializer data is valid
    if serializer.is_valid():
        # Save the user to the database
        user = serializer.save()

        # Generate JWT tokens for the user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Prepare the response data
        response_data = {
            'access_token': access_token,
            'user': serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    # Return errors if serializer data is invalid
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API view to get a list of users
@api_view(['GET'])
def get_user_list(request):
    # Retrieve all users from the database
    users = CustomUser.objects.all()
    
    # Serialize the users' data
    serializer = UserSerializer(users, many=True)
    
    # Return the serialized data as a response
    return Response(serializer.data)
