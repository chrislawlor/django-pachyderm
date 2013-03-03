import uuid

from django.test import TestCase

from pachyderm.fields import UUIDField

from test_app.models import UUIDContainerNonPK, UUIDContainerPK


class UUIDFieldTests(TestCase):
    
    def test_non_uuid_argument(self):
        field = UUIDField()
        with self.assertRaises(ValueError):
            field.get_prep_value('not a uuid')
    
    def test_get_prep_value(self):
        field = UUIDField(primary_key=True)
        self.assertTrue(field.primary_key == True)
        value = field.get_prep_value(None)
        self.assertTrue(value is None)
        id = uuid.uuid4()
        value = field.get_prep_value(id)
        self.assertEqual(id, value)
        
    def test_auto_pk(self):
        container = UUIDContainerPK.objects.create(name='container')
        #self.assertTrue(container.id is not None)
        self.assertTrue(type(container.id) is uuid.UUID)
        id = container.id
        retrieved = UUIDContainerPK.objects.get(name='container')
        self.assertEqual(container.id, retrieved.id)
    
    def test_non_pk(self):
        u = uuid.uuid4()
        container = UUIDContainerNonPK.objects.create(name='container',
                                                      uuid=u)
        self.assertEqual(1, UUIDContainerNonPK.objects.all().count())
        retrieved = UUIDContainerNonPK.objects.get(name='container')
        self.assertEqual(u, retrieved.uuid)