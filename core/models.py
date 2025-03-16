from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Subgroup(models.Model):
    name = models.CharField(max_length=50)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

