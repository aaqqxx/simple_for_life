import matplotlib.pyplot as plt
import matplotlib

# A range of values
x = list(range(0, 20))

# y = x^2
y = [xv * xv for xv in x]

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)

# Plot a line showing the curve
ax.plot(x, y)

for i in range(0, len(x) - 1):
    pt=(x[i],y[i])
    x_offset=5
    y_offset=5


    # Manual transformation fo the point
    # pt_tx = ax.transData.transform(pt)
    pt_tx = (x[i] + x_offset, y[i] + y_offset)

    # A circle drawn automatically in the data coordinates (blue-ish)
    ax.add_artist(plt.Circle(pt, 1, color="#00ffff"))

    # A circle drawn at my manually transformed coordinates (green)
    # I expect these should end up in the same position as the blue
    # ax.add_artist(plt.Circle(pt_tx, 4, transform=matplotlib.transforms.IdentityTransform(), color="#00ff00"))
    ax.add_artist(plt.Circle(pt_tx, 1,  color="#00ff00"))

#fig.savefig("test.pdf")
plt.show()