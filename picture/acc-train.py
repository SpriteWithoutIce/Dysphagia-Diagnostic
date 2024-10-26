import matplotlib.pyplot as plt

points = [(5, 58.13), (25, 85), (50, 87.5),
          (100, 90.62), (150, 91.25), (200, 93.75)]

x_coords, y_coords = zip(*points)

plt.figure()

plt.rcParams['font.family'] = 'arial'
plt.rcParams['font.size'] = 16

plt.plot(x_coords, y_coords, marker='o', color='#ff6043',
         label='Our Model')

plt.ylim(50, 100)

plt.xticks(x_coords)

plt.legend()
plt.xlabel('Number of Training Sample Per Subject',
           fontname='Arial', fontsize=16)
plt.ylabel('Classification Accuracy', fontname='Arial', fontsize=16)


plt.grid(False)
plt.savefig('acc_train.png')
