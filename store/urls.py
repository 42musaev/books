from rest_framework.routers import SimpleRouter

from store.views import BookViewSet

router = SimpleRouter()
router.register(r'book', BookViewSet, basename='book')

urlpatterns = []
urlpatterns += router.urls
