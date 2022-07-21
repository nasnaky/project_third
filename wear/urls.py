from django.urls import path, include
from .views import UserCreate, login, User_check, logout, User_update, Product_Detail, Product_type_list, \
    Product_title_list, Check_product_list, Basker_data, buy_up_create, Basker_deleta, Basket_buy_up_create \
    , buy_set_create
from rest_framework import routers

from django.conf.urls.static import static
from django.conf import settings

routers = routers.DefaultRouter()
routers.register('', User_update, basename='User')

urlpatterns = [
    path('user/', UserCreate),  # 회원 가입
    path('user/', include(routers.urls)),  # 회원 정보 수정

    path('Tch/', User_check),  # 로그인 확인

    path('login/', login),  # 로그인
    path('logout/', logout),  # 로그 아웃

    # path('cp/', coupon_list),

    path('kind/<str:type>/<int:pk>', Product_Detail),  # 제품 상세 정보
    path('kind/<str:type>', Product_type_list),  # 제품 종류 목록
    path('pro/<str:serch>', Product_title_list),  # 제품 제목 검색

    path('Ck/', Check_product_list),  # 찜 목록 추과 및 리스트

    path('BK/', Basker_data),  # 장바구니 목록 및 장바구니 리스트
    path('BK/<int:pk>', Basker_deleta),  # 장바구니 삭제
    path('BUY_BK/', Basket_buy_up_create),  # 장바구니 구매

    # path('BUY/<int:pk>', buy_up_bata),  # 즉시 구매 제품 리스트
    path('BUY/RE/', buy_set_create),
    path('BUY/', buy_up_create),  # 즉시 구매

]
urlpatterns += static('/media/', document_root=settings.MEDIA_ROOT)
