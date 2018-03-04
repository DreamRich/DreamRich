import inspect


class MetaTestsGenerator(type):

    def __init__(cls, name, bases, cls_dict):
        # Starts on PermissionsTestsSuite children classes
        children_hierarchy_depth = 3

        if len(cls.mro()) > children_hierarchy_depth:
            cls.generate_tests()

        super(MetaTestsGenerator, cls).__init__(name, bases, cls_dict)


class PermissionsTestsSuite(metaclass=MetaTestsGenerator):

    @classmethod
    def generate_tests(cls):
        template_methods_names = cls.get_template_methods_names()

        for template_method in template_methods_names:
            for action, status_code in cls.expected_status_codes:
                def test_action(self, template_method=template_method,
                                action=action, status_code=status_code):
                    test_method = getattr(self, template_method)
                    test_method(action, status_code)

                test_name = cls.get_test_name(template_method, action)
                setattr(cls, test_name, test_action)

    @classmethod
    def get_template_methods_names(cls):
        methods = inspect.getmembers(cls, predicate=inspect.isroutine)
        template_methods_names = [method[0] for method in methods
                                  if method[0].find('template') == 0]

        return template_methods_names

    @staticmethod
    def get_test_name(template_method_name, action):
        suffix = template_method_name.partition('_')[-1]
        return suffix + '_' + action


class AuthenticatedTests(PermissionsTestsSuite):

    def template_test_authenticated(self, action, status_code):
        self.user_test_request(action, status_code)


class UnauthenticatedTests(PermissionsTestsSuite):

    def template_test_unauthenticated(self, action, unused_status_code):
        self.user_test_not_authenticated_request(action)
