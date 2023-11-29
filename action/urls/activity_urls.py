from django.urls import path

from action import views

activity_patterns = [
    path('<int:pk>', views.ActivityDetailView.as_view(), name='detail'),
    path('manage/', views.ActivityManageView.as_view(), name='manage'),
    path('create/', views.ActivityCreateView.as_view(), name='create'),
    path('edit/<int:activity_id>', views.ActivityEditView.as_view(), name='edit'),

    path('delete/<int:activity_id>', views.activity.redirects.ActivityDeleteView.as_view(), name='delete_activity'),

    path('participate/<int:activity_id>', views.activity.redirects.ActivityParticipateView.as_view(), name='participate'),
    path('leave/<int:activity_id>', views.activity.redirects.ActivityLeaveView.as_view(), name='leave'),
    path('favorite/<int:activity_id>', views.activity.redirects.ActivityFavoriteView.as_view(), name='favorite'),
    path('unfavorite/<int:activity_id>', views.activity.redirects.ActivityUnfavoriteView.as_view(), name='unfavorite'),
]
