from json import dumps as json_dumps


from rest_framework.renderers import JSONRenderer

# {"user": {"detail": "Authentication error. The token cannot be decoded (FFF)"}}


class UserJSONRenderer(JSONRenderer):
    charset = "utf-8"
    base = "user"

    def render(self, data: dict, media_type=None, renderer_context: dict = None):
        # TODO: refactor

        # request = renderer_context.get("request", None)
        # response = renderer_context.get("response", None)

        # print(request.method == "DELETE")
        # print(response.status_code == HTTP_403_FORBIDDEN)

        errors = data.get("errors", None)

        if errors is not None:
            return super(UserJSONRenderer, self).render(data)

        self.launch_handlers(data)

        return json_dumps({self.base: data})

    def launch_handlers(self, data: dict):
        self.handle_byte_token_as_str(data, "access_token")
        self.handle_byte_token_as_str(data, "refresh_token")

    def handle_byte_token_as_str(self, data: dict, token_name: str):
        token = data.get(token_name, None)

        if token is not None and isinstance(token, bytes):
            data[token_name] = token.decode("utf-8")
