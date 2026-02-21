from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from framework.tests import BaseTestCase
from apps.breeding import factories, models
from apps.users.factories import UserFactory
from apps.animal.models import Animal


class BreedingTestCase(BaseTestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=UserFactory())

    def test_list_breeding_pair_should_success(self):
        factories.BreedingPairFactory()
        factories.BreedingPairFactory()

        response = self.client.get(reverse('breedingpair-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['total'], 2)

    def test_retrieve_breeding_pair_should_success(self):
        pair = factories.BreedingPairFactory()
        factories.BreedingPairFactory()

        response = self.client.get(reverse('breedingpair-detail', kwargs={'pk': pair.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['id'], str(pair.id))

    def test_create_breeding_pair_should_success(self):
        male = factories.AnimalFactory(sex=Animal.Sex.MALE)
        female = factories.AnimalFactory(sex=Animal.Sex.FEMALE)
        response = self.client.post(reverse('breedingpair-list'), data={
            'code': 'test_code_001',
            'male': male.id,
            'female': female.id,
            'paring_date': '2025-09-09',
            'status': models.BreedingPair.BreedingResult.IN_PROGRESS,
            'note': 'test note',
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        created_id = response.data['id']
        pair = models.BreedingPair.objects.get(id=created_id)
        self.assertEqual(pair.code, 'test_code_001')
        self.assertEqual(pair.male, Animal.Sex.MALE)
        self.assertEqual(pair.female, Animal.Sex.FEMALE)
        self.assertEqual(pair.paring_date, '2025-09-09')
        self.assertEqual(pair.status, models.BreedingPair.BreedingResult.IN_PROGRESS)
        self.assertEqual(pair.note, 'test note')

    def test_update_breeding_pair_should_success(self):
        pair = factories.BreedingPairFactory()
        male = factories.AnimalFactory(sex=Animal.Sex.MALE)
        female = factories.AnimalFactory(sex=Animal.Sex.FEMALE)
        response = self.client.patch(reverse('breedingpair-detail', kwargs={'pk': pair.id}), data={
            'code': 'test_code_001',
            'male': male.id,
            'female': female.id,
            'paring_date': '2025-09-09',
            'status': models.BreedingPair.BreedingResult.IN_PROGRESS,
            'note': 'test note',
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        pair.refresh_from_db()
        self.assertEqual(pair.code, 'test_code_001')
        self.assertEqual(pair.male, Animal.Sex.MALE)
        self.assertEqual(pair.female, Animal.Sex.FEMALE)
        self.assertEqual(pair.paring_date, '2025-09-09')
        self.assertEqual(pair.status, models.BreedingPair.BreedingResult.IN_PROGRESS)
        self.assertEqual(pair.note, 'test note')

    def test_delete_breeding_pair_should_success(self):
        pair = factories.BreedingPairFactory()
        response = self.client.delete(reverse('breedingpair-detail', kwargs={'pk': pair.id}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.data)
        self.assertFalse(models.BreedingPair.objects.actives().filter(id=pair.id).exists())