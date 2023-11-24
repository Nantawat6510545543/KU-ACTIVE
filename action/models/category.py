from django.db import models


class Category(models.Model):
    """Represents a category for activities."""

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        """
        Return a string representation of the category name.

        Returns:
            str: The name of the category.
        """
        return self.name
