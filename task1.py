import random
import datetime

n = 1

while n <= 10:
    random_year = random.randrange(2000,2024)
    random_month = random.randrange(1,12)
    random_day = random.randrange(1,29)
    first_random = random.random()
    second_random = random.randrange(1, 10)
    random_date = datetime.date(random_year,random_month,random_day)
    print('TODAY IS ', random_date)
    print('Random number between 0 and 1 is {:3.2f} '.format(first_random))
    print('Random number between 1 and 10 is %d' % second_random)
    print('*' * 44)
    n += 1
    
print('Random number program ENDED!')

