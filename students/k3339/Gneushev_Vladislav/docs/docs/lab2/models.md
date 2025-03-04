### Пользователь (`User`)
```
class User(AbstractUser):
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
```
### Авиакомпания (`Airline`)
```
class Airline(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)

    def __str__(self):
        return self.name
```
### Гейт (`Gate`)
```
class Gate(models.Model):
    number = models.CharField(max_length=10, unique=True, null=False)

    def __str__(self):
        return self.number
```
### Рейс (`Flight`)
```
class Flight(models.Model):
    class FlightType(models.TextChoices):
        ARRIVAL = 'arrival'
        DEPARTURE = 'departure'

    flight_number = models.CharField(max_length=10, unique=True, null=False)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    from_city = models.CharField(max_length=100, null=False)
    to_city = models.CharField(max_length=100, null=False)
    start_at = models.DateTimeField(null=False)
    end_at = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=10, choices=FlightType.choices, null=False)
    gate = models.ForeignKey(Gate, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.flight_number} {self.airline.name}'
```
### Билет (`Ticket`)
```
class Ticket(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    passenger = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=4, null=False, unique=True)

    def __str__(self):
        return f'Flight "{self.flight.flight_number}", ' \
               f'seat "{self.seat_number}" reserved ' \
               f'by "{self.passenger.username}"'
```
### Отзыв (`Review`)
```
class FlightReview(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    author = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['flight', 'author'],
                name='uk__flight_review'
            )
        ]

    def __str__(self):
        return f'"{self.author.username}" review for ' \
               f'flight "{self.flight.flight_number}"'
```