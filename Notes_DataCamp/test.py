import time
times = []
spam = []

first = input("")
f = time.time()
times.append(f)
while True:
    if time.time() - f >= 15:
        f = time.time()
        times = []
        spam = []
    user = input("")
    times.append(time.time())
    if len(times) == 5:
        for i in times:
            if int(i) - f <= 15:
                spam.append("spam")
        if len(spam) == 5:
            print("SPAM")
            f = time.time()
            times = []
            spam = []