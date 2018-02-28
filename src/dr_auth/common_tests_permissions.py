class MetaTestsGenerator(type):

    def __init__(cls, name, bases, unused_dict):
        if len(cls.mro()) > 2:  # Start on children classes
            cls.generate_tests()

        super(MetaTestsGenerator, cls).__init__(name, bases, dict)


class AuthenticatedTests(metaclass=MetaTestsGenerator):

    @classmethod
    def generate_tests(cls):
        if cls.expected_status_codes:
            for action, status_code in cls.expected_status_codes:
                def test_action(self):
                    # pylint: disable=cell-var-from-loop
                    self.user_test_request(action, status_code)

                test_name = 'test_' + action
                setattr(AuthenticatedTests, test_name, test_action)
        else:
            raise AttributeError(
                "For using 'AuthenticatedTests', the class must"
                " set a 'expected_status_codes' attribute."
            )


class NotAuthenticatedTests:
    # pylint: disable=not-callable

    user_test_not_authenticated_request = None  # pylint: disable=invalid-name

    def test_user_retrieve_list_not_authenticated(self):
        self.user_test_not_authenticated_request('list')

    def test_user_retrieve_not_authenticated(self):
        self.user_test_not_authenticated_request('retrieve')

    def test_user_create_not_authenticated(self):
        self.user_test_not_authenticated_request('create')

    def test_user_delete_not_authenticated(self):
        self.user_test_not_authenticated_request('destroy')

    def test_user_update_not_authenticated(self):
        self.user_test_not_authenticated_request('update')

    def test_user_partial_update_not_authenticated(self):
        self.user_test_not_authenticated_request('partial_update')
