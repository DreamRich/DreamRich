from django.test import TestCase
from client.factories import ActiveClientFactory
from client.views import ActiveClientViewSet
from .permissions_tests_utils import PermissionsTests


class TestPermissionsTests(TestCase):

    class UserToClient(PermissionsTests):
        factory_consulted = ActiveClientFactory
        factory_user = ActiveClientFactory
        view_consulted = ActiveClientViewSet

    def setUp(self):
        self.permission_test_class = self.UserToClient()
        self.permission_test_class.setUp()

        self.view_consulted = self.permission_test_class.view_consulted
        self.serializer_class = self.view_consulted.serializer_class
        self.factory_consulted = self.permission_test_class.factory_consulted

    def test_get_data(self):
        # pylint: disable=protected-access
        data = self.permission_test_class._get_data()
        # pylint: disable=protected-access

        self.assertEqual(
            list(data),
            ['name', 'surname', 'birthday', 'profession', 'cpf', 'telephone',
             'hometown', 'email', 'is_active']
        )

    def test_remove_read_only_fields(self):
        read_only_fields = [
            'pk', 'addresses', 'dependents', 'id_document', 'proof_of_address',
            'invalid', 'bank_account', 'invalid2', 'spouse', 'is_complete'
        ]

        data = self.serializer_class(self.factory_consulted()).data

        # pylint: disable=protected-access
        remove_read_only_fields = \
            self.permission_test_class._remove_read_only_fields
        data = remove_read_only_fields(data, read_only_fields)
        # pylint: disable=protected-access

        fields_names = list(data)
        for field in read_only_fields:
            self.assertNotIn(field, fields_names)

    def test_get_read_only_fields(self):
        serialized_class = self.serializer_class(self.factory_consulted())
        fields = serialized_class.get_fields()

        # pylint: disable=protected-access
        get_read_only_fields = self.permission_test_class._get_read_only_fields
        read_only_fields = get_read_only_fields(fields)
        read_only_fields_names = list(read_only_fields)
        # pylint: disable=protected-access

        self.assertEqual(
            read_only_fields_names,
            ['pk', 'addresses', 'dependents', 'id_document',
             'proof_of_address', 'bank_account', 'spouse', 'is_complete']
        )
