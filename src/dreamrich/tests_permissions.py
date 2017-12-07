import json
from django.test import TestCase
from rest_framework.test import APIClient
from .utils import authenticate_user

class PermissionsTests(TestCase):

    def setUp(self):
        self._initialize()

    def _initialize(self):
        self.django_client = APIClient()

        self.user = self.factory()
        self.consulted_instance = self.user.id
        
        authenticate_user(self.user)

    def user_get_list_request(self, status_code):
        response_status_code = self.make_request("get_list")
        self.assertEqual(response_status_code, status_code)

    def user_get_request(self, status_code):
        response_status_code = self.make_request("get")
        self.assertEqual(response_status_code, status_code)

    def user_post_request(self, status_code):
        response_status_code = self.make_request("post")
        self.assertEqual(response_status_code, status_code)

    def user_delete_request(self, status_code):
        response_status_code = self.make_request("delete")
        self.assertEqual(response_status_code, status_code)

    def user_put_request(self, status_code):
        response_status_code = self.make_request("put")
        self.assertEqual(response_status_code, status_code)

    def user_patch_request(self, status_code):
        response_status_code = self.make_request("patch")
        self.assertEqual(response_status_code, status_code)

    def make_request(self, test_type):
        test_types = ["get", "put", "patch", "delete", "post", "get_list"]
        require_data_methods = ["put", "patch", "post"]

        if test_type not in test_types:
            raise AttributeError("Invalid http method")

        if test_type == "get_list":
            http_method = "get"
        else:
            http_method = test_type

        method = getattr(self.django_client, http_method)
        route = self._get_route(test_type)

        # Prepare data and make request
        if test_type in require_data_methods:
            data = self.serializer(self.user).data

            # Send data just to one field
            if method == "patch":
                data = data.popitem()
                data = {k: v for k, v in data}

            data = json.dumps(data)
            response = method(route, data, content_type='application/json')
        else:
            response = method(route)

        return response.status_code

    def _get_route(self, test_type):
        general_routes_tests = ["post", "get_list"]

        if test_type not in general_routes_tests:
            route = '{}{}/'.format(self.base_route, self.consulted_instance)

        return route
