from game import board
import tensorflow

def accuracy(real, output, covered):
    ans = real.copy()
    for i in range(len(real)):
        for j in range(len(real[0])):
            ans[i][j] = f'r{real[i][j]} o{output[i][j]} {'c' if covered[i][j] == -1 else 'u'}'
    return ans

e = board.generateForData(30, 16, 99)
c = board.random_coverage(e)

model = tensorflow.keras.models.load_model("model.keras")

feed = board.set_dimensions(c)
ans = model.predict(feed)
print(ans.shape)
ans = [[round(float(val), 2) for val in row] for row in ans.squeeze()]
print('----Grid Fed In-------------------------------------------------------------------')
for r in c:
    frmt = "{:>11}" * len(r)
    print(frmt.format(*r))
print('----Grid Fed In Uncovered-------------------------------------------------------------------')
for r in e:
    frmt = "{:>11}" * len(r)
    print(frmt.format(*r))
print('-------Result----------------------------------------------------------------')
for r in ans:
    frmt = "{:>11}" * len(r)
    print(frmt.format(*r))
print('------Accuracy Grid-----------------------------------------------------------------')
for r in accuracy(board.create_label_grid(e), ans, c):
    frmt = "{:>11}" * len(r)
    print(frmt.format(*r))
