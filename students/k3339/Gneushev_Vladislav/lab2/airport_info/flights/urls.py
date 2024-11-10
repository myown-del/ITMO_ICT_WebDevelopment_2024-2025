from django.urls import path

from . import views

urlpatterns = [
    path('', views.FlightsList.as_view(), name='flights_list'),
    path('<int:flight_id>/', views.flight_detail, name='flight_details'),
    path('<int:flight_id>/reserve/', views.reserve_ticket, name='reserve_ticket'),
    path('ticket/edit/<int:ticket_id>/', views.edit_ticket, name='edit_ticket'),
    path('ticket/delete/<int:ticket_id>/', views.delete_ticket, name='delete_ticket'),
    path('flight/<int:flight_id>/add_review/', views.add_review, name='add_review'),
]
