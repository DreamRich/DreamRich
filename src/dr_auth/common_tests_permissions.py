class NotAuthenticatedTests:
    # pylint: disable=not-callable

    user_test_not_authenticated_request = None  # pylint: disable=invalid-name

    def test_user_get_list_not_authenticated(self):
        self.user_test_not_authenticated_request('list')

    def test_user_get_not_authenticated(self):
        self.user_test_not_authenticated_request('retrieve')

    def test_user_post_not_authenticated(self):
        self.user_test_not_authenticated_request('create')

    def test_user_delete_not_authenticated(self):
        self.user_test_not_authenticated_request('destroy')

    def test_user_put_not_authenticated(self):
        self.user_test_not_authenticated_request('update')

    def test_user_patch_not_authenticated(self):
        self.user_test_not_authenticated_request('partial_update')


class NotAuthenticatedToItselfTests:
    # pylint: disable=not-callable

    user_test_not_authenticated_request = None  # pylint: disable=invalid-name

    def test_user_get_not_authenticated(self):
        self.user_test_not_authenticated_request('retrieve')

    def test_user_delete_not_authenticated(self):
        self.user_test_not_authenticated_request('destroy')

    def test_user_put_not_authenticated(self):
        self.user_test_not_authenticated_request('update')

    def test_user_patch_not_authenticated(self):
        self.user_test_not_authenticated_request('partial_update')
