import json
from django.shortcuts import redirect
from django.urls import reverse
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
from django.core.mail import EmailMultiAlternatives

renderer = JSONRenderer()



from rest_framework.authtoken.views import ObtainAuthToken, APIView
from django.views.decorators.csrf import csrf_exempt

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
            return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.email_confirmed:
            return JsonResponse({'error': 'Email address not validated'}, status=status.HTTP_403_FORBIDDEN)
        
        token, _ = Token.objects.get_or_create(user=user)
        return JsonResponse({
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
    serializer_class = EmailSerializer

    def perform_create(self, serializer):
        to = serializer.validated_data['to']
        subject = serializer.validated_data['subject']
        message = serializer.validated_data['message']

        try:
            send_mail(subject, message, 'friess.heinz@gmx.de', [to], fail_silently=False)
        except Exception as e:
            return JsonResponse({"message": "Email could not be sent", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
def register(request):  
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed for registration.'}, status=405)
    # Parse JSON data manually
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Invalid JSON data provided.'}, status=400)
    
    # Handle the registration process
    try:
        new_user = CustomUser.objects.create_user(username=username, email=email, password=password)
    except Exception as e:
        return JsonResponse({'message': 'Username allready exists', "error": str(e)}, status=401)
    
    email = createMail(new_user, request)
    
    try:
        email.send()
        return JsonResponse({            
            'emailIsSend': True,
            'email': new_user.email
        }, status=status.HTTP_200_OK)
    except Exception as e:
            return JsonResponse({"message": "Email could not be sent", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def createMail(new_user, request):
    # Build email confirmation
    token = default_token_generator.make_token(new_user)
    uid = urlsafe_base64_encode(force_bytes(new_user.pk))
    email_subject = 'Activate your account'
    
    # Construct activation link
    activation_link = request.build_absolute_uri(reverse('activate_account', kwargs={'uidb64': uid, 'token': token}))
    email_body = render_to_string('email_confirmation.html', {
        'user': new_user,
        'activation_link': activation_link,
    })
    # Create an EmailMultiAlternatives object
    email = EmailMultiAlternatives(
        email_subject,
        '',
        'friess.heinz@gmx.de',
        [new_user.email]
    )

    # Attach the HTML content to the email
    email.attach_alternative(email_body, 'text/html')

    return email
    
    
    


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.email_confirmed = True
        user.save()
        return redirect('https://videoflix.heinzfriess.com')
    else:
        return JsonResponse({'message' : 'Activation link is invalid!'})
