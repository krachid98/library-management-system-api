from django.urls import path
from .views import RegisterView, LoginView, LogoutView, LibroView, LibroGetDetails, PreferitiViewSet

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('books/', LibroView.as_view(), name='libro-list'),
    path("books/<int:id>/", LibroGetDetails.as_view(), name="book-detail"),
    path('favorites/', PreferitiViewSet.as_view({'get': 'list'}), name='list-favorites'),
    path('favorites/<int:book_id>/', PreferitiViewSet.as_view({'post': 'create', 'delete': 'destroy'}), name='modify-favorite'),
]