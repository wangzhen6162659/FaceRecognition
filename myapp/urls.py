from django.conf.urls import url, include
import myapp.views

urlpatterns = [
url(r'add_book$', myapp.views.add_book, ),
url(r'show_books$', myapp.views.show_books, ),
url(r'get_face$', myapp.views.get_face, ),
]