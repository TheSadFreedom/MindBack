from json import dumps as json_dumps


from rest_framework.exceptions import ErrorDetail
from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnList


class NeuralNetworkJSONRenderer(JSONRenderer):
    charset = "utf-8"
    base = "neural_network"

    # TODO: refactor
    def render(self, data, media_type=None, renderer_context=None):
        # request = renderer_context.get("request", None)
        # response = renderer_context.get("response", None)

        # print(request.method == "DELETE")
        # print(response.status_code == HTTP_403_FORBIDDEN)

        if self.is_error_or_detail_info(data):
            errors = data.get("errors", None)

            if errors is not None:
                return super(NeuralNetworkJSONRenderer, self).render(data)

            self.handle_not_found(data)
        elif self.is_list_of_neural_networks(data):
            self.convert_base_to_plural(self.base)

        return json_dumps({self.base: data})

    def handle_not_found(self, data: dict):
        detail = data.get("detail", None)

        if detail is not None and detail.code == "not_found":
            data["errors"] = ErrorDetail(
                string="Нейронная сеть не найдена!", code=detail.code
            )
            data.pop("detail")

    def is_list_of_neural_networks(self, data) -> bool:
        return type(data) is ReturnList

    def is_error_or_detail_info(self, data) -> bool:
        return type(data) is dict

    def convert_base_to_plural(self, base: str) -> str:
        self.base += "s"
