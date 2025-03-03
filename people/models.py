from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=100)

    birth_year = models.IntegerField(null=True, blank=True)
    birth_month = models.IntegerField(null=True, blank=True)
    birth_day = models.IntegerField(null=True, blank=True)

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

    def get_birthday_display(self):
        """생일 정보를 표시 형식으로 반환합니다."""
        parts = []
        if self.birth_year:
            parts.append(f"{self.birth_year}년")
        if self.birth_month:
            parts.append(f"{self.birth_month}월")
        if self.birth_day:
            parts.append(f"{self.birth_day}일")
        return " ".join(parts) if parts else "생일 정보 없음"
