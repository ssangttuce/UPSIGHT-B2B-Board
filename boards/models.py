from django.db import models
from django.utils import timezone
from authentication.models import Business, BusinessMember

class Post(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(BusinessMember, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_public = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def soft_delete(self):
        """Marks the post as deleted by setting deleted_at to current time."""
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        """Restores the post by setting deleted_at to None."""
        self.deleted_at = None
        self.save()

    @property
    def is_deleted(self):
        """Checks if the post is marked as deleted."""
        return self.deleted_at is not None

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(BusinessMember, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    is_public = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def soft_delete(self):
        """Marks the comment as deleted by setting deleted_at to current time."""
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        """Restores the comment by setting deleted_at to None."""
        self.deleted_at = None
        self.save()

    @property
    def is_deleted(self):
        """Checks if the comment is marked as deleted."""
        return self.deleted_at is not None
