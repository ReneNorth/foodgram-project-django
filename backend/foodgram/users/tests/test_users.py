from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


# class RecipeTest(TestCase):
#     @classmethod
#     def setUpClass(cls) -> None:
#         super().setUpClass()
#         cls.author = User.objects.create(
#             email='vpupkin7@yandex.ru',
#             username='vasya7.pupkin',
#             first_name='Вася6',
#             last_name='Пупкин6',
#             password='Qwerty12323'
#         )

#     @classmethod
#     def tearDownClass(cls):
#         """Вызывается один раз после запуска всех тестов класса."""
#         print('>> tearDownClass')
#         cls.author.destroy()
#         super().tearDownClass()

#         """Вызывается после каждого теста."""

#     def tearDown(self):
#         self.author.destroy()
#         print('>>> tearDown')

#     def test_user_created(self):
#         try:
#             self.assertAlmostEqual(
#                 User.objects.count(), 1)
#         except Exception as e:
#             assert False, f'{e} nope'
