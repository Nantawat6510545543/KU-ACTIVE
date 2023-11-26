from django.urls import path

from action import views

friends_patterns = [
    path('', views.FriendView.as_view(), name='friends'),

    path('add/', views.AddFriendView.as_view(), name='add_view'),
    path('add/<int:friend_id>/', views.add_friend, name='add_friend'),
    path('remove/<int:friend_id>/', views.remove_friend, name='remove_friend'),

    path('requests/', views.RequestView.as_view(), name='request_view'),
    path('requests/accept/<int:friend_id>', views.accept_request, name='accept_request'),
    path('requests/decline/<int:friend_id>', views.decline_request, name='decline_request'),
    path('requests/cancel/<int:friend_id>', views.cancel_request, name='cancel_request'),
]
