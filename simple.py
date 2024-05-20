import fastchan

tx, rx = fastchan.bounded(10)

tx.send(1)
tx.send("hi")

del tx

for x in rx:
    print(x)

del rx
