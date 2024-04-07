from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=100)

    birth_year = models.IntegerField()
    birth_month = models.IntegerField()
    birth_day = models.IntegerField()

    mother = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children_mother",
    )
    father = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children_father",
    )

    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
