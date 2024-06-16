import pandas as pd
#任务一
#导入CSV文件
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.unicode.east_asian_width', True)
df1 = pd.read_csv(r'movie_metadata\movie_metadata.csv' , encoding='gbk')

#将数据保存为excel
df1.to_excel('movie_metadata.xlsx' , index=False)

#任务二
# 检查缺失值
print("缺失值检查:")
print(df1.isna().sum())
# 检查重复值
print("\n重复值检查:")
print(df1.duplicated().sum())
#同时删除缺失值和重复值
df_clean = df1.dropna().drop_duplicates()
# 展示处理后的数据前5到10条
print("\n处理后的数据前7条:")
print(df_clean.head(7))
#将数据保存为excel
df_clean.to_excel('movie_metadata_clean1.xlsx' , index=False)

#任务三
# （1）按照导演进行分组查看总票房
grouped_by_director = df_clean.groupby('director_name')['gross'].sum().reset_index()
# 展示处理后的数据前7条
print("\n按照导演进行分组查看总票房处理后的数据前7条:")
print(grouped_by_director.head(7))
#将数据保存为excel
grouped_by_director.to_excel('total_box_office_by_director.xlsx', index=False)

# （2）按照第一位演员进行分组查看总票房
grouped_by_actor1 = df_clean.groupby('actor_1_name')['gross'].sum().reset_index()
# 展示处理后的数据前6条
print("\n按照第一位演员进行分组查看总票房处理后的数据前6条:")
print(grouped_by_actor1.head(6))
#将数据保存为excel
grouped_by_actor1.to_excel('total_box_office_by_actor.xlsx', index=False)

# （3）按照导演与演员的搭配分组并查看总票房
# 假设使用actor_1_name作为搭配的主要演员
grouped_by_director_actor = df_clean.groupby(['director_name', 'actor_1_name'])['gross'].sum().reset_index()
# 展示处理后的数据前6条
print("\n按照导演与第一位演员的搭配分组查看总票房处理后的数据前6条:")
print(grouped_by_director_actor.head(6))
#将数据保存为excel
grouped_by_director_actor.to_excel('total_box_office_by_director_actor.xlsx', index=False)

#任务四
# 创建一个函数，用于获取每个导演的最高和最低票房电影
def get_extreme_movies_by_director(group):
    # 找到最高和最低票房的索引
    max_gross_idx = group['gross'].idxmax()
    min_gross_idx = group['gross'].idxmin()

    # 提取最高和最低票房电影的信息
    max_movie = group.loc[max_gross_idx]
    min_movie = group.loc[min_gross_idx]

    # 将这些信息组合成一个Series
    extreme_movies = pd.Series({
        'director_name': group.name,
        'highest_gross_movie_title': max_movie['movie_title'],  # 假设这里有一个名为'movie_title'的列
        'highest_gross': max_movie['gross'],
        'highest_gross_year': max_movie['title_year'],
        'highest_gross_language': max_movie['language'],
        'highest_gross_country': max_movie['country'],
        'lowest_gross_movie_title': min_movie['movie_title'],
        'lowest_gross': min_movie['gross'],
        'lowest_gross_year': min_movie['title_year'],
        'lowest_gross_language': min_movie['language'],
        'lowest_gross_country': min_movie['country'],
        # ... 可以继续添加其他列 ...
    })

    # 将Series转换为DataFrame，以便后续操作
    return extreme_movies.to_frame().T


# 使用groupby和apply函数应用上面的函数
extreme_movies_df = df_clean.groupby('director_name').apply(get_extreme_movies_by_director, include_groups=False).reset_index(drop=True)
# 展示处理后的数据前6条
print("\n按照获取每个导演的最高和最低票房电影并展示其他信息的处理后的数据前6条:")
print(extreme_movies_df.head(6))
#将数据保存为CSV
extreme_movies_df.to_csv('extreme_movies_df.csv', index=False)

#任务五
# 选择与电影类型和受欢迎程度相关的列
relevant_columns = ['genres', 'gross', 'imdb_score', 'movie_facebook_likes']
df_for_analysis = df_clean[relevant_columns]

# 假设genres列可能包含多个电影类型，用逗号分隔
# 我们需要拆分这个列，并展开数据以便可以按类型分组

def split_genres(genres):
    return genres.split(',')

# 应用split_genres函数到genres列，并展开DataFrame
genres_exploded = df_for_analysis['genres'].str.split(',', expand=True).stack().reset_index(level=1, drop=True).rename(
    'genre')
df_genres_exploded = df_for_analysis.drop('genres', axis=1).join(genres_exploded)

# 按genre分组并计算指标
grouped = df_genres_exploded.groupby('genre').agg({
    'gross': 'mean',  # 平均票房
    'imdb_score': 'mean',  # 平均IMDb评分
    'movie_facebook_likes': 'sum'  # 所有电影在Facebook上的总点赞数
}).reset_index()
# 展示处理后的数据前6条
print("\n按照基于电影类型的数据分析，查看不同类型电影的受欢迎的处理后的数据前6条:")
print(grouped.head(6))
# 保存结果到CSV文件
grouped.to_csv('popularity_by_genre.csv', index=False)
#good
#goood