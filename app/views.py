from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import *
import json
import traceback
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("🔵 Received data:", data)

            device_id = data.get('Device_id')
            user_name = data.get('User_name')
            password = data.get('password')
            mob = data.get('Mob')
            email = data.get('Email')

            if not all([device_id, user_name, mob, email]):
                return JsonResponse({'error': 'Device_id, User_name, Mob, and Email are required.'}, status=400)

            if MyUser.objects.filter(Device_id=device_id).exists():
                return JsonResponse({'error': 'Device_id already exists.'}, status=409)

            if MyUser.objects.filter(Mob=mob).exists():
                return JsonResponse({'error': 'Mobile number already registered.'}, status=409)

            if MyUser.objects.filter(Email=email).exists():
                return JsonResponse({'error': 'Email already registered.'}, status=409)

            user = MyUser.objects.create(
                Device_id=device_id,
                User_name=user_name,
                password=password,
                Mob=mob,
                Email=email
            )

            return JsonResponse({
                'message': 'User created successfully.',
                'Device_id': user.Device_id,
                'User_name': user.User_name,
                'Mob': user.Mob,
                'Email': user.Email
            }, status=201)

        except Exception as e:
            print("🔥 Exception:", str(e))
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid HTTP method. Use POST.'}, status=405)



@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            identifier = data.get('identifier')
            password = data.get('password')

            if not all([identifier, password]):
                return JsonResponse({'error': 'Username/Email/Mobile and password are required.'}, status=400)

            try:
                # Determine login method
                if identifier.isdigit():
                    user = MyUser.objects.get(Mob=int(identifier))
                elif '@' in identifier:
                    user = MyUser.objects.get(Email=identifier)
                else:
                    user = MyUser.objects.get(User_name=identifier)

                if user.password == password:
                    return JsonResponse({
                        'message': 'Login successful',
                        'Device_id': user.Device_id,
                        'User_name': user.User_name,
                        'Mob': user.Mob,
                        'Email': user.Email
                    }, status=200)
                else:
                    return JsonResponse({'error': 'Invalid password'}, status=401)

            except MyUser.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def forgot_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')

            if not email:
                return JsonResponse({'error': 'Email is required.'}, status=400)

            try:
                user = MyUser.objects.get(Email=email)
                reset_link = f"{settings.BASE_URL}/reset-password/?email={user.Email}"


                from django.core.mail import send_mail
                send_mail(
                    subject="Reset Your Password",
                    message=f"Hi {user.User_name},\n\nClick the link to reset your password:\n{reset_link}",
                    from_email="care.bariflolabs@gmail.com",
                    recipient_list=[user.Email],
                    fail_silently=False,
                )


                return JsonResponse({'message': 'Reset link sent to your email.'}, status=200)

            except MyUser.DoesNotExist:
                return JsonResponse({'error': 'Email not found.'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


@csrf_exempt
def reset_password(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            new_password = data.get('new_password')

            if not all([email, new_password]):
                return JsonResponse({'error': 'Email and new password are required.'}, status=400)

            try:
                user = MyUser.objects.get(Email=email)
                user.password = new_password
                user.save()
                return JsonResponse({'message': 'Password updated successfully.'}, status=200)

            except MyUser.DoesNotExist:
                return JsonResponse({'error': 'User with this email not found.'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)




@csrf_exempt
def reset_password_page(request):
    email = request.GET.get('email', '')
    return render(request, 'reset_password.html', {'email': email})






@csrf_exempt
def post_alert(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            device_id = data.get('device_id')
            alert_message = data.get('alert_message')
            time_stamp = data.get('Time_stamp')

            if not all([device_id, alert_message, time_stamp]):
                return JsonResponse({'error': 'device_id, alert_message, and Time_stamp are required.'}, status=400)

            try:
                user = MyUser.objects.get(Device_id=device_id)
            except MyUser.DoesNotExist:
                return JsonResponse({'error': f'Device {device_id} not found'}, status=404)

            alert = Alert(Device_id=user, alert_message=alert_message, Time_stamp=time_stamp)
            alert.save()

            return JsonResponse({'message': 'Alert saved successfully.', 'id': alert.id}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid HTTP method. Only POST is allowed.'}, status=405)
