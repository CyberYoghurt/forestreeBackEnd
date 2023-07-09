from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.response import Response

from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse

from .serializer import UserMachinerySerializer, UserWoodSerializer, UserSerializer, WoodSerializer, WoodListSerializer, MachinerySerializer, MachineryListSerializer, ProductListSerializer
from .models import Wood, Machinery, Product

from django.contrib.auth.models import User

from chat.models import Chat
from chat.serializer import ChatListSerializer

import stripe

# Create your views here.


class WoodPage(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        try:
            received_page = request.GET.get('page', 1)
            woods = Wood.objects.all()
            wood_paginator = Paginator(woods, 1)
            woods_of_page = wood_paginator.page(received_page)
            woods_serializer = WoodListSerializer(
                woods_of_page.object_list, many=True)
            response = {
                'numberOfPages': int(wood_paginator.num_pages),
                'hasNext': woods_of_page.has_next(),
                'hasPrevious': woods_of_page.has_previous(),
                'providers': woods_serializer.data
            }
            return JsonResponse(response, status=200, safe=False)
        except Exception as e:
            return JsonResponse(str(e), status=500, safe=False)

    def post(self, request):
        try:
            info = (request.data.dict())

            info['owner'] = request.user.id
            wood_serializer = WoodSerializer(data=info)
            if (wood_serializer.is_valid()):
                wood_serializer.save()
                return JsonResponse(wood_serializer.data, status=200)
            else:
                return JsonResponse(wood_serializer.errors, status=400)
        except Exception as E:
            return Response(status=500)


class MachineryPage(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        try:
            received_page = request.GET.get('page', 1)
            machineries = Machinery.objects.all()
            machinery_paginator = Paginator(machineries, 1)
            machineries_of_page = machinery_paginator.page(received_page)
            machinery_serializer = MachineryListSerializer(
                machineries_of_page.object_list, many=True)
            response = {
                'numberOfPages': int(machinery_paginator.num_pages),
                'hasNext': machineries_of_page.has_next(),
                'hasPrevious': machineries_of_page.has_previous(),
                'providers': machinery_serializer.data
            }
            return JsonResponse(response, status=200, safe=False)
        except Exception as e:
            return JsonResponse(str(e), status=500)

    def post(self, request):
        try:
            info = (request.data.dict())
            info['owner'] = request.user.id
            machinery_serializer = MachinerySerializer(data=info)
            if (machinery_serializer.is_valid()):
                machinery_serializer.save()
                return JsonResponse(machinery_serializer.data, status=200)
            else:
                return JsonResponse(machinery_serializer.errors, status=400)
        except Exception as E:
            return JsonResponse({'error': str(E)}, status=500)


class WoodInfo(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        received_id = request.GET.get('id', 1)
        id = int(received_id)
        wood = Wood.objects.filter(id=id)[0]
        wood_serialized = WoodListSerializer(wood, many=False)
        return JsonResponse(wood_serialized.data, status=200, safe=False)

    def delete(self, request):
        id = request.data['id']

        return Response(status=200)


class MachineryInfo(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        received_id = request.GET.get('id', 1)
        id = int(received_id)
        machinery = Machinery.objects.filter(id=id)[0]
        machinery_serialized = MachinerySerializer(machinery, many=False)
        return JsonResponse(machinery_serialized.data, status=200, safe=False)


class Shop(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        try:
            page_number = request.GET.get('page', 1)
            all_products = Product.objects.all()
            paginator = Paginator(all_products, 4)
            products = paginator.page(page_number)
            product_serialized = ProductListSerializer(
                products.object_list, many=True)
            response = {
                'numberOfPages': int(paginator.num_pages),
                'hasNext': products.has_next(),
                'hasPrevious': products.has_previous(),
                'products': product_serialized.data
            }
            return JsonResponse(response, status=200, safe=False)

        except Exception as E:
            return Response(status=404)

    def post(self, request):
        info = request.data.dict()
        product_serialized = ProductListSerializer(data=info)
        if (product_serialized.is_valid()):
            product_serialized.save()
            return JsonResponse(data=product_serialized.data, status=200)
        else:
            return JsonResponse(product_serialized.errors, status=400)


class CheckOut(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        try:
            info = (request.data)
            total_price = 0
            for item in info:
                total_price += (float(item['price']) - (float(item['price'])
                                * float(item['discount']))) * float(item['quantity'])

            total_price = round(total_price, 2)
            stripe.api_key = 'sk_test_51MlFqGI12VwHEyX8tE3PF8Id3fGSPM2dM9ff2QwDi7vnjFTdbrIOnudbNrmxZkqmZBHPDpk4S9t9hhnGYDWAUfuX00UjwQ7rLP'
            # Create a PaymentIntent with the order amount and currency
            intent = stripe.PaymentIntent.create(
                amount=int(total_price * 100),
                currency='usd',
                automatic_payment_methods={
                    'enabled': True,
                },
            )
            return JsonResponse({'clientSecret': intent['client_secret']}, status=200)

        except Exception as e:
            return Response(status=403)


class ChatInfo(APIView):
    permission_classes = [AllowAny]

    # Get the chats where is a user has joined
    def get(self, request):
        user = request.user
        chats = user.user_chats.all()
        chats_serialized = ChatListSerializer(chats, many=True)
        return JsonResponse(data=chats_serialized.data, status=200, safe=False)

    # Create a chat between users
    def post(self, request):
        contact = User.objects.get(id=request.data['ownerId'])
        user = request.user

        try:
            if (contact.id == user.id):
                raise Exception('You Cant message yourself')

            chat_name = str(contact.id) + 'and' + str(user.id)

            foundChat = Chat.objects.filter(name=chat_name)
            if (len(foundChat) > 0):

                # return Response(status=200)
                return JsonResponse(data={'name': chat_name}, status=200)

            new_chat = Chat(name=chat_name)
            new_chat.save()
            new_chat.users.add(contact)
            new_chat.users.add(user)
            return JsonResponse(data={'name': chat_name}, status=200)

        except Exception as e:
            return Response(status=400)


class ParseUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return HttpResponse(status=200)


class ManageUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        userSerialized = UserSerializer(request.user)
        woods = Wood.objects.filter(owner=request.user)
        machineries = Machinery.objects.filter(owner=request.user)

        # finding and appending the suppliers this has created
        woods_serialized = UserWoodSerializer(woods, many=True)
        machineries_serialized = UserMachinerySerializer(
            machineries, many=True)

        # userSerialized.data['woods'] = woods_serialized.data
        # userSerialized.data['machineries'] = machineries_serialized.data

        data = {
            'userInfo': userSerialized.data,
            'woods': woods_serialized.data,
            'machineries': machineries_serialized.data
        }

        return JsonResponse(data=data, status=200, safe=False)

    def patch(self, request):
        return Response(status=200)
