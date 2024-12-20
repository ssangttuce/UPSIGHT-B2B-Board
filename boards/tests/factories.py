import factory
from factory import Faker
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model
from boards.models import Business, Post, Comment
from django.utils import timezone

User = get_user_model()

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker('user_name')
    password = factory.PostGenerationMethodCall('set_password', 'password123!')
    role = 'member'  # 기본 역할을 BUSINESS_MEMBER로 설정

class BusinessFactory(DjangoModelFactory):
    class Meta:
        model = Business

    name = Faker('company')

class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    title = Faker('sentence', nb_words=6)
    content = Faker('paragraph', nb_sentences=3)
    is_public = True
    deleted_at = None
    author = factory.SubFactory(UserFactory)
    business = factory.SubFactory(BusinessFactory)
    
class PublishedPostFactory(PostFactory):
    is_public = True
    deleted_at = None

class DraftPostFactory(PostFactory):
    is_public = False
    deleted_at = None

class DeletedPostFactory(PostFactory):
    is_public = False
    deleted_at = factory.LazyFunction(timezone.now)

class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    content = Faker('sentence', nb_words=100)
    is_public = True
    deleted_at = None
    author = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)