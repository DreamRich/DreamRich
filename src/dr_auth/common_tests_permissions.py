from dreamrich.requests import RequestTypes


class NotAuthenticatedTests:
    # pylint: disable=not-callable

    user_test_not_authenticated_request = None  # pylint: disable=invalid-name

    def test_user_get_list_not_authenticated(self):
        self.user_test_not_authenticated_request(RequestTypes.GETLIST)

    def test_user_get_not_authenticated(self):
        self.user_test_not_authenticated_request(RequestTypes.GET)

    def test_user_post_not_authenticated(self):
        self.user_test_not_authenticated_request(RequestTypes.POST)

    def test_user_delete_not_authenticated(self):
        self.user_test_not_authenticated_request(RequestTypes.DELETE)

    def test_user_put_not_authenticated(self):
        self.user_test_not_authenticated_request(RequestTypes.PUT)

    def test_user_patch_not_authenticated(self):
        self.user_test_not_authenticated_request(RequestTypes.PATCH)


class NotAuthenticatedToItselfTests:
    # pylint: disable=not-callable

    user_test_not_authenticated_request = None  # pylint: disable=invalid-name

    def test_user_get_not_authenticated(self):
        self.user_test_not_authenticated_request(RequestTypes.GET)

    def test_user_delete_not_authenticated(self):
        self.user_test_not_authenticated_request(RequestTypes.DELETE)

    def test_user_put_not_authenticated(self):
        self.user_test_not_authenticated_request(RequestTypes.PUT)

    def test_user_patch_not_authenticated(self):
        self.user_test_not_authenticated_request(RequestTypes.PATCH)
