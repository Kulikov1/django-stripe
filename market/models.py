from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    price = models.IntegerField()
    currency = models.CharField(max_length=3)

    class Meta:
        verbose_name = ('item')
        verbose_name_plural = ('items')

    def __str__(self):
        return self.name


class Order(models.Model):

    class Meta:
        verbose_name = ('order')
        verbose_name_plural = ('orders')

    def __str__(self):
        return f'Order №{self.pk}'


class ItemInOrder(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ('ItemInOrder')
        verbose_name_plural = ('ItemsInOrder')

    def __str__(self):
        return self.item.name
