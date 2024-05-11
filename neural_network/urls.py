from rest_framework.routers import SimpleRouter


from .views import NeuralNetworkViewSet


app_name = "neural_network"

router = SimpleRouter()

router.register(f"{app_name}s", NeuralNetworkViewSet)
router.register(f"v1/{app_name}s", NeuralNetworkViewSet)

urlpatterns = router.urls
