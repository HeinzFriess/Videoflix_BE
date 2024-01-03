import json
from django.shortcuts import render
from videoflix.serializers import SignupSerializer,UsersSerializer, EmailSerializer
from users.models import CustomUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status,generics
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer

renderer = JSONRenderer()



from rest_framework.authtoken.views import ObtainAuthToken, APIView

# Create your views here.

class UserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        users = CustomUser.objects.all()
        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):  # , *args, **kwargs):
        data = {
            'username': request.data.get('username'),
            #'first_name': request.data.get('first_name'),
            #'last_name': request.data.get('last_name'),
            'email': request.data.get('email')
        }
        serializer = UsersSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        #user = serializer
        token, created = Token.objects.get_or_create(user=serializer) # user=user
        return Response({
            'token': token.key,
            'user_id': serializer.pk, #user.pk
            'email': serializer.email #user.email
        })


class loginview(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=username, email=email, password=password)
        print(user)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.email_confirmed:
            return Response({'error': 'Email address not validated'}, status=status.HTTP_403_FORBIDDEN)
        
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'user_id': user.pk,
            'token': token.key,
            'email': user.email
            }, status=status.HTTP_202_ACCEPTED)


class signupview(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = SignupSerializer

class adduserview(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    #serializer_class = SignupSerializer

    serializer_class = EmailSerializer

    def perform_create(self, serializer):
        to = serializer.validated_data['to']
        subject = serializer.validated_data['subject']
        message = serializer.validated_data['message']

        try:
            send_mail(subject, message, 'friess.heinz@gmx.de', [to], fail_silently=False)
        except Exception as e:
            return Response({"message": "Email could not be sent", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def register(request):  
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed for registration.'}, status=405)
    # Parse JSON data manually
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        # Handle the registration process
        new_user = CustomUser.objects.create_user(username=username, email=email, password=password)
        # Rest of your email sending logic...
        # Send email confirmation
        token = default_token_generator.make_token(new_user)
        uid = urlsafe_base64_encode(force_bytes(new_user.pk))
        email_subject = 'Activate your account'
        email_body = render_to_string('email_confirmation.html', {
            'user': new_user,
            'uid': uid,
            'token': token,
        })
        try:
            send_mail(email_subject, email_body, 'friess.heinz@gmx.de', [new_user.email], fail_silently=False)
            return JsonResponse({            # Redirect to a page indicating that the email has been sent
                'emailIsSend': True,
                'email': new_user.email
            }, status=status.HTTP_200_OK)
        except Exception as e:
                return JsonResponse({"message": "Email could not be sent", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        

    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Invalid JSON data provided.'}, status=400)
    except KeyError as e:
        return JsonResponse({'error': f'Missing key in JSON data: {str(e)}'}, status=400)
    


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.email_confirmed = True
        user.save()
        # You can redirect to a page indicating successful activation
        return JsonResponse({'message' : 'Your account has been activated successfully!' })
    else:
        # Handle invalid activation link/token
        return JsonResponse({'message' : 'Activation link is invalid!'})
