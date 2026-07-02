from django.conf import settings
from django.db import models


class Bounty(models.Model):
    STATUS_CHOICES = [
        ('wanted', 'Wanted'),
        ('captured', 'Captured'),
    ]

    target_name = models.CharField(max_length=255)
    reward = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='wanted',
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bounties',
    )


    description = models.TextField(blank=True, default='')
    location = models.CharField(max_length=255, blank=True, default='')
    danger_level = models.CharField(
        max_length=20,
        blank=True,
        default='',
        help_text="e.g. 'low', 'medium', 'high', 'legendary'",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.target_name} ({self.status}) — ${self.reward}"