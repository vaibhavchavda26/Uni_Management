from pprint import pprint
from django.shortcuts import render,HttpResponse, redirect,HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login

from .serializers import PrincipalSerializer, UserSerializer
from .models import User, Teachers, Students, Principal
from django.contrib import messages
from rest_framework.views import APIView 

from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

class Index(APIView):
	def index(request):
		return render(request, "index.html")


class Contact(APIView):
	def contact(request):
		return render(request, 'contact.html')

class LoginUser(APIView):
	def loginUser(request):
		return render(request, 'login_page.html')


class DoLogin(APIView):

	def doLogin(request):
		print("here")
		email_id = request.GET.get('email')
		password = request.GET.get('password')
		# user_type = request.GET.get('user_type')
		print(email_id)
		print(password)
		print(request.user)
		if not (email_id and password):
			messages.error(request, "Please provide all the details!!")
			return render(request, 'login_page.html')

		user = User.objects.filter(email=email_id, password=password).last()
		if not user:
			messages.error(request, 'Invalid Login Credentials!!')
			return render(request, 'login_page.html')

		login(request, user)
		print(request.user)

		if user.user_type == User.STUDENT:
			return redirect('student_home/')
		elif user.user_type == User.TEACHERS:
			return redirect('staff_home/')
		elif user.user_type == User.PRINCIPAL:
			return redirect('admin_home/')

		return render(request, 'home.html')

class Registration(APIView):	
	def registration(request):
		return render(request, 'registration.html')
	
class DoRegistration(APIView):	
	def doRegistration(request):
		first_name = request.GET.get('first_name')
		last_name = request.GET.get('last_name')
		email_id = request.GET.get('email')
		password = request.GET.get('password')
		confirm_password = request.GET.get('confirmPassword')

		print(email_id)
		print(password)
		print(confirm_password)
		print(first_name)
		print(last_name)
		if not (email_id and password and confirm_password):
			messages.error(request, 'Please provide all the details!!')
			return render(request, 'registration.html')
	
		if password != confirm_password:
			messages.error(request, 'Both passwords should match!!')
			return render(request, 'registration.html')

		is_user_exists = User.objects.filter(email=email_id).exists()

		if is_user_exists:
			messages.error(request, 'User with this email id already exists. Please proceed to login!!')
			return render(request, 'registration.html')

		user_type = GetUserTypeFromEmail(email_id)

		if user_type is None:
			messages.error(request, "Please use valid format for the email id: '<username>.<teacher|student|principal>@<college_domain>'")
			return render(request, 'registration.html')

		username = email_id.split('@')[0].split('.')[0]

		if User.objects.filter(username=username).exists():
			messages.error(request, 'User with this username already exists. Please use different username')
			return render(request, 'registration.html')

		user = User()
		user.username = username
		user.email = email_id
		user.password = password
		user.user_type = user_type
		user.first_name = first_name
		user.last_name = last_name
		user.save()
	
		if user_type == User.TEACHERS:
			Teachers.objects.create(admin=user)
		elif user_type == User.STUDENT:
			Students.objects.create(admin=user)
		elif user_type == User.PRINCIPAL:
			Principal.objects.create(admin=user)
		return render(request, 'login_page.html')

class Logout(APIView):	
	def logout_user(request):
		logout(request)
		return HttpResponseRedirect('/')

class GetUserTypeFromEmail(APIView):
	def get_user_type_from_email(email_id):

		try:
			email_id = email_id.split('@')[0]
			email_user_type = email_id.split('.')[1]
			return User.EMAIL_TO_USER_TYPE_MAP[email_user_type]
		except:
			return None


class List(APIView):
	def get(self, request, pk=None, format=None):
		id = pk
		if id is not None:
			user = User.objects.get(id=id)
			serializer = UserSerializer(user)
			return Response(serializer.data)
			
		user = User.objects.all()
		serializer = UserSerializer(user, many = True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = UserSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({'msg':'Data created'}, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def put(self, request, pk, format=None):
		id = pk
		user = User.objects.get(pk = id)
		serializer = UserSerializer(user, data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({'msg':'Complete Data Updated'})
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def patch(self, request, pk, format=None):
		id = pk
		user = User.objects.get(pk=id)
		serializer = UserSerializer(user, data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({'msg':'Partial Data Updated'})
		return Response(serializer.errors)

	def delete(self, request, pk, format=True):
		id = pk
		users = User.objects.get(pk=id)
		users.delete()
		return Response({'msg': 'Data Deleted'})


