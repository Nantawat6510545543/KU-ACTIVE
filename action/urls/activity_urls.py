from django.urls import path

from action import views

activity_patterns = [
    path('<int:pk>', views.ActivityDetailView.as_view(), name='detail'),
    path('manage/', views.ActivityManageView.as_view(), name='manage'),
    path('create/', views.ActivityCreateView.as_view(), name='create'),
    path('edit/<int:activity_id>', views.ActivityEditView.as_view(), name='edit'),

    path('delete/<int:activity_id>', views.delete_activity, name='delete_activity'),

    path('participate/<int:activity_id>', views.participate, name='participate'),
    path('leave/<int:activity_id>', views.leave, name='leave'),
    path('favorite/<int:activity_id>', views.favorite, name='favorite'),
    path('unfavorite/<int:activity_id>', views.unfavorite, name='unfavorite'),
]
