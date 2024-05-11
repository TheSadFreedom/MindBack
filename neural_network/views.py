from django.utils.decorators import method_decorator


from drf_yasg.utils import swagger_auto_schema

from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT


from .models import NeuralNetwork
from .permissions import AuthorOrIsAuthenticated, AuthorOrNotHidden
from .renderers import NeuralNetworkJSONRenderer
from .serializers import NeuralNetworkSerializer


# TODO: add pagination
# TODO: add form load in swagger
# TODO: develop swagger
# TODO: add logo delete for neuro
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(auto_schema=None),
)
class NeuralNetworkViewSet(ModelViewSet):
    renderer_classes = (NeuralNetworkJSONRenderer,)
    queryset = NeuralNetwork.objects.all()
    serializer_class = NeuralNetworkSerializer
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    actions_permissions = {
        "list": (AllowAny,),
        "retrieve": (AuthorOrNotHidden,),
    }
    default_permission = (AuthorOrIsAuthenticated,)

    def get_queryset(self):
        return self.queryset

    def get_permissions(self):
        permission_classes = self.actions_permissions.get(
            self.action, self.default_permission
        )
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["GET"], permission_classes=[AuthorOrIsAuthenticated])
    def author_list(self, request: Request, *args, **kwargs):
        """Get all neural network of current user"""
        neural_networks = self.queryset.filter(author=request.user)

        serializer = self.serializer_class(neural_networks, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["POST"], permission_classes=[AuthorOrIsAuthenticated])
    def logo(self, request: Request, *args, **kwargs):
        """Upload neural network's logo"""
        neural_network: NeuralNetwork = self.get_object()

        data = {"logo": request.FILES["logo"]}

        serializer = self.serializer_class(neural_network, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @swagger_auto_schema(security=[])
    def list(self, request: Request):
        """Get all neural networks"""
        neural_networks = self.queryset.filter(is_hidden=False)
        serializer = self.serializer_class(neural_networks, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(security=[])
    def retrieve(self, request: Request, pk=None):
        """Get neural network"""
        neural_network = self.get_object()
        serializer = self.serializer_class(neural_network)
        return Response(serializer.data)

    def partial_update(self, request: Request, pk=None):
        """Patch neural network"""
        neural_network = self.get_object()
        neural_network_data = request.data.get("neural_network", {})

        serializer = self.serializer_class(
            neural_network, data=neural_network_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def create(self, request: Request, *args, **kwargs):
        """Create neural network"""
        neural_network = request.data.get("neural_network", {})

        serializer = self.serializer_class(data=neural_network)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)

        return Response(serializer.data, status=HTTP_201_CREATED)

    # TODO: add logic for safety removing
    def destroy(self, request: Request, pk=None):
        """Delete neural network"""
        neural_network: NeuralNetwork = self.get_object()

        neural_network.delete()

        return Response(status=HTTP_204_NO_CONTENT)
