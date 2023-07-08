from django.urls import path
from .views import ManageUser,WoodPage,MachineryPage,Shop,ParseUser,CheckOut,WoodInfo,MachineryInfo,ChatInfo,ParseUser

urlpatterns = [
    path('check/', ParseUser.as_view()),
    path('wood/', WoodPage.as_view()),
    path('woodInfo/',WoodInfo.as_view()),
    path('machinery/',MachineryPage.as_view()),
    path('machineryInfo/',MachineryInfo.as_view()),
    path('tool-shop/',Shop.as_view()),
    path('checkout/',CheckOut.as_view()),
    path('chat-info/',ChatInfo.as_view()),
    path('update/',ManageUser.as_view())

]