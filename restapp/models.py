from django.db import models


class Products(models.Model):
    productName = models.CharField(max_length=150)
    productCategory = models.CharField(max_length=100)
    productCount = models.IntegerField()

    def __str__(self):
        return self.productName

    class Meta:
        db_table = "Products"
