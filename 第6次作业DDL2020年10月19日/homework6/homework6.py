import numpy as np
import pandas as pd
import math
import csv


# 根据余弦算相似度
def calCosineSimilarity(list1, list2):
    res = 0
    denominator1 = 0
    denominator2 = 0
    for (val1, val2) in zip(list1, list2):
        res += (val1 * val2)
        denominator1 += val1 ** 2
        denominator2 += val2 ** 2
    return res / (math.sqrt(denominator1 * denominator2))


# 读入数据
moviesPath = 'movies.csv'
ratingsPath = 'ratings.csv'
# 电影的dataframe
moviesDF = pd.read_csv(moviesPath, index_col=None)
# 评分的dataframe
ratingsDF = pd.read_csv(ratingsPath, index_col=None)

# 生成用户id和电影id对于评分的透视表
ratingsPivotDF = pd.pivot_table(ratingsDF[['userId', 'movieId', 'rating']], columns=['movieId'], index=['userId'],
                                values='rating', fill_value=0)
# 将透视表转化为list
ratingValues = ratingsPivotDF.values.tolist()
print('step0')

# 电影map
moviesMap = dict(enumerate(list(ratingsPivotDF.columns)))

# 用户map
usersMap = dict(enumerate(list(ratingsPivotDF.index)))

print(len(ratingValues))

# 初始化相似度矩阵均为0.0
userSimMatrix = np.zeros((len(ratingValues), len(ratingValues)), dtype=np.float32)
print(len(userSimMatrix))

# 计算相似矩阵
for i in range(len(ratingValues) - 1):
    for j in range(i + 1, len(ratingValues)):
        userSimMatrix[i, j] = calCosineSimilarity(ratingValues[i], ratingValues[j])
        userSimMatrix[j, i] = userSimMatrix[i, j]
        print('processing' + str(i) + ' ' + str(j))
print('step1')

# 选出每个用户相似度最高的十个用户
userMostSimDict = dict()
for i in range(len(ratingValues)):
    userMostSimDict[i] = sorted(enumerate(list(userSimMatrix[0])), key=lambda x: x[1], reverse=True)[:10]
print('step2')

# 初始化推荐值为0
userRecommendValues = np.zeros((len(ratingValues), len(ratingValues[0])), dtype=np.float32)

# 如果看过电影，推荐值就是0；否则就是10个相似用户的相似度和评分的积的累加和除以10个相似用户的相似度的累加和
for i in range(len(ratingValues)):
    for j in range(len(ratingValues[i])):
        if ratingValues[i][j] == 0:
            val = 0
            val1 = 0
            for (user, sim) in userMostSimDict[i]:
                val1 += (ratingValues[user][j] * sim)
            val2 = 0
            for (user, sim) in userMostSimDict[i]:
                val2 += sim
            val = val1 / val2
            userRecommendValues[i, j] = val
            print('processing' + str(i) + ' ' + str(j))
print('step3')

# 取出推荐值最高的电影
userRecommendDict = dict()
for i in range(len(ratingValues)):
    userRecommendDict[i] = sorted(enumerate(list(userRecommendValues[i])), key=lambda x: x[1], reverse=True)[:1]
print('step4')

# 转化为原来对应的id
userRecommendList = []
for key, value in userRecommendDict.items():
    user = usersMap[key]
    for (movieId, val) in value:
        userRecommendList.append([user, moviesMap[movieId]])
print('step5')

recommendDF = pd.DataFrame(userRecommendList, columns=['userId', 'movieId'])

# 根据用户id排序
recommendDF.sort_values("userId", inplace=True)
print('step6')

# 写入movie.csv文件
with open('movie.csv', "a+", encoding='UTF-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows([['userId', 'movieId']])
    for i in range(len(recommendDF)):
        index_val = recommendDF.index[i]
        row = recommendDF.loc[index_val].values.tolist()
        print(row)
        writer.writerows([[row[0], row[1]]])
