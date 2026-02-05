from decimal import Decimal
from django.db import models
from framework.models import BaseModel, BaseModelQuerySet
from apps.specie.models import Specie

class Animal(BaseModel):
    class Sex(models.TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'
    
    class Origin(models.TextChoices):
        WILD = 'wild', 'Wild'
        CAPITIVE = 'captive', 'Captive'

    class Status(models.TextChoices):
        KEEP = 'keep', 'Keep'
        BREED = 'breed', 'Breed'
        SELL = 'sell', 'Sell'
        SOLD = 'sold', 'Sold'
        DEAD = 'dead', 'Dead'

    code = models.CharField(max_length=512, help_text='animal code')
    specie = models.ForeignKey(Specie, null=True, blank=True, on_delete=models.CASCADE, related_name='animals')
    sex = models.CharField(choices=Sex.choices, null=True, blank=True, help_text='animal sex')
    hatch_date = models.DateField(null=True, blank=True, help_text='hacth date')
    acquisition_date = models.DateField(null=True, blank=True, help_text='date that coming to hand')
    origin = models.CharField(choices=Origin.choices, default=Origin.CAPITIVE, help_text='hatch place')
    egg = models.ForeignKey('breeding.EggBatch', null=True, blank=True, on_delete=models.CASCADE, related_name='animals')
    individual_feeding_plans = models.ManyToManyField('feeding.FeedingPlan', blank=True, related_name='individual_animals')
    genetic_value_note = models.TextField(null=True, blank=True, help_text='note for genetic information')
    status = models.CharField(choices=Status.choices, null=True, blank=True, default=Status.KEEP, help_text='keep status')
    is_assist_feed_needed = models.BooleanField(default=False, null=True, blank=True, help_text='if assit feeding is needed')
    note = models.TextField(null=True, blank=True, help_text='note')

    def __str__(self):
        return f"{self.code}"
    
    @property
    def is_dead(self):
        return self.dead_transaction is not None

    @property
    def father(self):
        pass

    @property
    def mother(self):
        pass
    
    @property
    def reproductive_availability(self):
        pass

    @property
    def grow_score(self):
        pass

    @property
    def feeding_score(self):
        pass

    @property
    def breeding_history_score(self):
        pass

    @property
    def wild_percentage(self):
        pass

    @property
    def generation_depth(self):
        pass

    @property
    def current_weight(self):
        pass

    @property
    def days_from_last_breed(self):
        pass

    @property
    def is_breed_available(self):
        pass

    @property
    def last_feeding_result(self):
        pass

    @property
    def active_feeding_plans(self):
        # if self.individual_feeding_plans.exists():
        #     return self.individual_feeding_plans.all()
        # return self.specie.feeding_plans.all()
        pass

    @property
    def all_applicable_plans(self):
        # return self.specie.feeding_plans.all() | self.individual_feeding_plans.all()
        pass
    
    # can not edit if dead
    
    class Meta:
        ordering = ['-created', '-updated']
        verbose_name = 'Animal'
        verbose_name_plural = 'Animals'


class SizeLogTransaction(BaseModel):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='size_logs')
    weight = models.DecimalField(max_digits=16, decimal_places=2, default=Decimal(0), help_text='weight measurement')
    length = models.DecimalField(max_digits=16, decimal_places=2, default=Decimal(0), help_text='length measurement')
    waist = models.DecimalField(max_digits=16, decimal_places=2, default=Decimal(0), help_text='waist measurement')
    date = models.DateField(help_text='measurement date')
    note = models.TextField(null=True, blank=True, help_text='note')

    def __str__(self):
        return f"{self.animal} - size log"
    
    class Meta:
        ordering = ['-created', '-updated']
        verbose_name = 'Size Log Transaction'
        verbose_name_plural = 'Size Log Transactions'


class FeedingLogTransaction(BaseModel):
    class FeedingType(models.TextChoices):
        FREE_FEED = 'free_feed', 'Free Feed'
        HAND_FEED = 'hand_feed', 'Hand Feed'
        FORCE_FEED = 'force_feed', 'Force Feed'

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='feeding_logs')
    food = models.ForeignKey('feeding.Food', on_delete=models.CASCADE, related_name='feeding_logs')
    amount = models.PositiveIntegerField(default=1, help_text='food amount')
    date = models.DateField(help_text='measurement date')
    feeding_type = models.CharField(null=True, blank=True, choices=FeedingType.choices, default=FeedingType.FREE_FEED, help_text='feeding type')
    note = models.TextField(null=True, blank=True, help_text='note')

    def __str__(self):
        return f"{self.animal} - {self.date} - feeding log"
    
    @property
    def amount_with_unit(self):
        return f"{self.amount} {self.food.unit}"
    
    class Meta:
        ordering = ['-created', '-updated']
        verbose_name = 'Feeding Log Transaction'
        verbose_name_plural = 'Feeding Log Transactions'

class FeedingResultLogTransaction(BaseModel):
    class Result(models.TextChoices):
        SUCCESS = 'success', 'Success'
        REFUSED = 'refuse', 'Refuse'
        PARTIAL = 'partial', 'Partial'
        REGURGITATION = 'regurgitation', 'regurgitation'

    transaction = models.ForeignKey(FeedingLogTransaction, on_delete=models.CASCADE, related_name='results')
    date = models.DateField(help_text='result marked date')
    result = models.CharField(choices=Result.choices, help_text='feeding result')
    note = models.TextField(null=True, blank=True, help_text='note')

    # if regurgitation is happend....

    def __str__(self):
        return f"{self.transaction.animal} - feeding log - {self.result}"
    
    class Meta:
        ordering = ['-created', '-updated']
        verbose_name = 'Feeding Result Log Transaction'
        verbose_name_plural = 'Feeding Result Log Transactions'


class DeadLogTransaction(BaseModel):
    class Cause(models.TextChoices):
        DISEASE = 'disease', 'Disease'
        ACCIDENT = 'accident', 'Accident'
        OLD_AGE = 'old_age', 'Old age'
        REPRODUCTIVE = 'reproductive', 'Reproductive issue'
        UNKNOWN = 'unknown', 'Unknown'

    animal = models.OneToOneField(Animal, on_delete=models.CASCADE, related_name='dead_log_transaction', help_text='detail of death')
    date = models.DateField(help_text='dead date')
    cause = models.CharField(null=True, blank=True, choices=Cause.choices, default=Cause.UNKNOWN, help_text='dead cause')
    note = models.TextField(null=True, blank=True, help_text='note')

    def __str__(self):
        return f"{self.animal} - {self.cause}"
    
    class Meta:
        ordering = ['-created', '-updated']
        verbose_name = 'Dead Log Transaction'
        verbose_name_plural = 'Dead Log Transactions'