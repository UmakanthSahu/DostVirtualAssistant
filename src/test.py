import random
income = ["high", "med", "low"]
age  = ["old", "adult", "young" ]
fond = ["yes", "no"]
freq = ["regular", "rare"]
purchase = ["high", "med", "low"]

for i in range(20):
    i = random.choice(income)
    a = random.choice(age)
    f = random.choice(fond)
    fr = random.choice(freq)
    p = random.choice(purchase)
    print(i,a,f,fr,p,sep=", ")