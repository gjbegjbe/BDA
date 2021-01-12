import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


iris = datasets.load_iris()
iris_feature = iris.data
iris_target = iris.target
iris_feature = iris_feature[:, 0:2]
feature_train, feature_test, target_train, target_test = train_test_split(iris_feature, iris_target, train_size=0.8, random_state=1)

# knn分类器
clf = KNeighborsClassifier()
clf.fit(feature_train, target_train.ravel())

x1_min, x1_max = iris_feature[:, 0].min(), iris_feature[:, 0].max()
x2_min, x2_max = iris_feature[:, 1].min(), iris_feature[:, 1].max()
xx, yy = np.mgrid[x1_min:x1_max:200j, x2_min:x2_max:200j]
grid_test = np.stack((xx.flat, yy.flat), axis=1)
grid_hat = clf.predict(grid_test)
grid_hat = grid_hat.reshape(xx.shape)

cm_light = mpl.colors.ListedColormap(['#A0FFA0', '#FFA0A0', '#A0A0FF'])
cm_dark = mpl.colors.ListedColormap(['g', 'r', 'b'])

plt.pcolormesh(xx, yy, grid_hat, shading='auto', cmap=cm_light)
plt.scatter(iris_feature[:, 0], iris_feature[:, 1], c=iris_target, edgecolors='k', s=50, cmap=cm_dark)
plt.scatter(feature_test[:, 0], feature_test[:, 1], s=120, facecolors='none', zorder=10)

plt.xlabel('Length', fontsize=13)
plt.ylabel('Width', fontsize=13)
plt.xlim(x1_min, x1_max)
plt.ylim(x2_min, x2_max)
plt.title('Iris KNN classifier', fontsize=15)
plt.grid(b=True, ls=':')
plt.savefig('knn.png')
plt.show()

print("The scores of train set is %f" % (clf.score(feature_train, target_train)))
print("The scores of test set is %f" % (clf.score(feature_test, target_test)))