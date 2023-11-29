from django.urls import path

from action import views

friends_patterns = [
    path('', views.FriendListView.as_view(), name='friends'),
    path('add/', views.AddFriendView.as_view(), name='add_view'),
    path('requests/', views.FriendRequestView.as_view(), name='request_view'),

    path('remove/<int:friend_id>/', views.friend.redirects.RemoveFriendView.as_view(), name='remove_friend'),
    path('requests/send/<int:friend_id>/', views.friend.redirects.SendRequestView.as_view(), name='send_request'),
    path('requests/accept/<int:friend_id>', views.friend.redirects.AcceptRequestView.as_view(), name='accept_request'),
    path('requests/decline/<int:friend_id>', views.friend.redirects.DeclineRequestView.as_view(), name='decline_request'),
    path('requests/cancel/<int:friend_id>', views.friend.redirects.CancelRequestView.as_view(), name='cancel_request'),
]
