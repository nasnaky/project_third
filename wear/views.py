from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.parsers import JSONParser
from django.db.models import Q
from datetime import date, timedelta
from rest_framework.decorators import api_view

import hashlib

from .models import User, Basket_buy, Basket, Product, Check_Product, buyReady

from .serializers import UserCreateSerializer, UserUpdateSerializer, ProductDetailSerializer, \
    ProductListSerializer, Check_ProductUPSerializer, Check_ProductListSeral, BaskerUPSerializer, BaskerListSerializer, \
    buyUPSerializer, Basket_buy_up_Serializer, buyReadySerializer, buySetSerializer


class check:

    def email_check(self):
        try:
            User.objects.get(email=self)
            return False
        except Exception:
            return True

    def token_check(self):
        accessToken = self.META.get('HTTP_AUTHORIZATION')
        refreshToken = self.META.get('HTTP_REFRESHTOKEN')
        try:
            user = User.objects.get(refreshToken=refreshToken)
            if user.accessToken == accessToken:
                return True
            return False
        except Exception:
            return False


@api_view(['POST'])  # 회원가입
def UserCreate(request):
    if request.method == "POST":
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            if check.email_check(email):
                email_name = email.split('@')
                name = email_name[0]
                refreshToken = hashlib.sha256(email.encode())
                serializer.save(name=name, accessToken="null",
                                max_day=date.today(),
                                refreshToken=str(refreshToken.hexdigest()))
                return Response({
                    "message": "회원가입이 되었습니다."
                })
            return Response({
                "message": "이미 사용 중인 이메일 입니다."
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "message": "잘못된 요청입니다."
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])  # 로그인
def login(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        email = data['email']
        search_email = email
        try:
            email = email + str(date.today())
            accessToken = hashlib.sha1(email.encode())
            same_email = User.objects.get(email=search_email)
            if data['password'] == same_email.password:
                same_email.accessToken = str(accessToken.hexdigest())
                same_email.max_day = date.today() + timedelta(days=30)
                same_email.save()
                return Response({
                    "accessToken": same_email.accessToken,
                    "refreshToken": same_email.refreshToken
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "message": "비밀번호가 틀렸습니다."
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({
                "message": "이메일이 틀렸습니다."
            }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])  # 로그 아웃
def logout(request):
    if request.method == "GET":
        accessToken = request.META.get('HTTP_AUTHORIZATION')
        user = User.objects.get(accessToken=accessToken)
        user.accessToken = "null"
        user.save()
        return Response({
            "message": "로그아웃이 되었습니다."
        })


@api_view(['GET'])  # 로그인 유지
def User_check(request):
    if request.method == "GET":
        if check.token_check(request):
            refreshToken = request.META.get('HTTP_REFRESHTOKEN')
            user = User.objects.get(refreshToken=refreshToken)
            accessToken = request.META.get('HTTP_AUTHORIZATION')
            if user.accessToken == accessToken:
                if user.max_day >= date.today():
                    return Response({
                        "message": "로그인이 유지 됩니다."
                    })
                return Response({
                    "message": "토큰이 만료 되었습니다."
                })


class User_update(viewsets.ModelViewSet):  # 데이터 수정
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        data = request.data
        if user.accessToken == request.META.get('HTTP_AUTHORIZATION'):
            if data['img'] != "":
                user.img = data['img']
            user.name = data['name']
            if user.email != data['email']:
                if check.email_check(data['email']):
                    user.email = data['email']
                else:
                    return Response({
                        "message": "이미 사용 중인 이메일입니다."
                    })
            if data['password'] != "":
                user.password = data['password']
            user.save()
            return Response({
                "message": "변경되었습니다."
            })
        return Response({
            "message": "accessToken 값이 다릅니다."
        })


# @api_view(['GET'])  # 쿠폰 리스트
# def coupon_list(request):
#    if request.method == "GET":
#        if check.token_check(request):
#            accessToken = request.META.get('HTTP_AUTHORIZATION')
#            user = User.objects.get(accessToken=accessToken)
#            list = Coupon.objects.filter(user_by=user)
#            serializer = CouponSerializer(list, many=True)
#            return Response(serializer.data)
#        return Response({
#            "message": "다시 로그인 하시길 바랍니다."
#        })


@api_view(['GET'])  # 제품 개인 객체
def Product_Detail(request, pk, type):
    if request.method == "GET":
        product = Product.objects.get(types=type, id=pk)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)


@api_view(['GET'])
def Product_type_list(request, type):  # 종류 검색
    if request.method == "GET":
        list = Product.objects.filter(types=type)
        serializer = ProductListSerializer(list, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def Product_title_list(request, serch):  # 제목 검색
    if request.method == "GET":
        list = Product.objects.filter(title__contains=serch)
        serializer = ProductListSerializer(list, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def Check_product_list(request):
    if request.method == "GET":  # 찜 목록
        if check.token_check(request):
            accessToken = request.META.get('HTTP_AUTHORIZATION')
            user = User.objects.get(accessToken=accessToken)
            list = Check_Product.objects.filter(user_by=user)
            serializer = Check_ProductListSeral(list, many=True)
            return Response(serializer.data)

    if request.method == "POST":  # 찜 목록 추과
        if check.token_check(request):
            serializer = Check_ProductUPSerializer(data=request.data)
            if serializer.is_valid():
                accessToken = request.META.get('HTTP_AUTHORIZATION')
                user = User.objects.get(accessToken=accessToken)
                product = serializer.validated_data.get('product')
                product = Product.objects.get(id=product)
                try:
                    objects = Check_Product.objects.get(user_by=user, product_by=product)
                    objects.delete()
                    return Response({
                        "message": "삭제돼었습니다."
                    })
                except Exception:
                    objects = Check_Product()
                    objects.user_by = user
                    objects.product_by = product
                    objects.save()
                    return Response({
                        "message": "등록돼었습니다."
                    })
            return Response({
                "message": "등록되지 못했습니다."
            })
        return Response({
            "message": "다시 로그인 하시길 바랍니다."
        })


@api_view(['POST', 'GET'])
def Basker_data(request):  # 장바구니 등록
    if request.method == "POST":
        if check.token_check(request):
            serializer = BaskerUPSerializer(data=request.data)
            if serializer.is_valid():
                accessToken = request.META.get('HTTP_AUTHORIZATION')
                user = User.objects.get(accessToken=accessToken)
                product = serializer.validated_data.get('product_by')
                product = Product.objects.get(id=product)
                objects = Basket()
                objects.user_by = user
                objects.product_by = product
                objects.size = serializer.validated_data.get('size')
                objects.colors = serializer.validated_data.get('colors')
                objects.save()
                return Response({
                    "message": "등록됐습니다."
                })
            return Response({
                "message": "등록되지 못했습니다."
            })
        return Response({
            "message": "다시 로그인 하시길 바랍니다."
        })

    if request.method == "GET":  # 장바구니 목록
        if check.token_check(request):
            if check.token_check(request):
                accessToken = request.META.get('HTTP_AUTHORIZATION')
                user = User.objects.get(accessToken=accessToken)
                list = Basket.objects.filter(Q(user_by=user) and Q(Basket_buy_by=None))
                serializer = BaskerListSerializer(list, many=True)
                return Response(serializer.data)
            return Response({
                "message": "다시 로그인 하시길 바랍니다."
            })


@api_view(['DELETE'])  # 장바구니 삭제
def Basker_deleta(request, pk):
    if request.method == "DELETE":
        if check.token_check(request):
            basker = Basket.objects.get(id=pk)
            basker.delete()
            return Response({
                "message": "삭제되었습니다."
            })
        return Response({
            "message": "다시 로그인 하시길 바랍니다."
        })


@api_view(['GET', 'POST'])  # 바로 구매 준비
def buy_set_create(request):
    if request.method == "GET":
        if check.token_check(request):
            accessToken = request.META.get('HTTP_AUTHORIZATION')
            user = User.objects.get(accessToken=accessToken)
            pro = buyReady.objects.filter(user=user).latest('id')
            Serializer = buySetSerializer(pro)
            return Response(Serializer.data)
        return Response({
            "message": "다시 로그인 하시길 바랍니다."
        })
    if request.method == "POST":
        Serializer = buyReadySerializer(data=request.data)
        if Serializer.is_valid():
            if check.token_check(request):
                accessToken = request.META.get('HTTP_AUTHORIZATION')
                user = User.objects.get(accessToken=accessToken)
                id = Serializer.validated_data.get('product')
                pro = Product.objects.get(id=id)
                objects = buyReady()
                objects.user = user
                objects.product = pro
                objects.size = Serializer.validated_data.get('size')
                objects.colors = Serializer.validated_data.get('colors')
                objects.save()
                return Response(status=status.HTTP_200_OK)
            return Response({
                "message": "다시 로그인 하시길 바랍니다."
            })


@api_view(['POST'])  # 바로 구매
def buy_up_create(request):
    if request.method == "POST":
        if check.token_check(request):
            serializer = buyUPSerializer(data=request.data)
            if serializer.is_valid():
                accessToken = request.META.get('HTTP_AUTHORIZATION')
                user = User.objects.get(accessToken=accessToken)
                product = serializer.validated_data.get('product')
                product = Product.objects.get(id=product)
                serializer.save(user=user, product=product)
                return Response({
                    "message": "구매가 완료되었습니다."
                })
            return Response({
                "message": "구매가 완료되지 않았습니다."
            })
        return Response({
            "message": "다시 로그인 하시길 바랍니다."
        })


# @api_view(['GET'])  # 바로 구매 리스트
# def buy_up_bata(request, pk):
#     if request.method == "GET":
#         if check.token_check(request):
#             product = Product.objects.get(id=pk)
#             serializer = ProductListSerializer(product)
#             return Response(serializer.data)
#         return Response({
#             "message": "다시 로그인 하시길 바랍니다."
#         })


@api_view(['POST'])
def Basket_buy_up_create(request):
    if request.method == "POST":
        if check.token_check(request):
            serializer = Basket_buy_up_Serializer(data=request.data)
            if serializer.is_valid():
                accessToken = request.META.get('HTTP_AUTHORIZATION')
                user = User.objects.get(accessToken=accessToken)
                serializer.save(user=user)
                buy_list = Basket.objects.filter(Q(user=user) and Q(Basket_buy_by=None))
                buy = Basket_buy.objects.filter(user=user).order_by('-bate').first()
                for i in buy_list:
                    i.Basket_buy_by = buy
                    i.save()
                return Response({
                    "message": "구매가 완료되었습니다."
                })
            return Response({
                "message": "구매가 완료되지 않았습니다."
            })
        return Response({
            "message": "다시 로그인 하시길 바랍니다."
        })
