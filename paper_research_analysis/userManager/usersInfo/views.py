from django.shortcuts import render
# pandas用于解析读取excel数据
import pandas as pd
from pathlib import Path
import time
# Redis数据库操作引入
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.http import HttpResponse
# MySQL数据库操作引入
from django.db import models

# Create your views here.

'''读取excel数据'''
def read_excel():
    # 2.把Excel文件中的数据读入pandas
    BASE_DIR = Path(__file__).resolve().parent
    excel_url = str(BASE_DIR) + '\\world-universities.xlsx' 
    # print(BASE_DIR)
    df = pd.read_excel(excel_url)
    print(df)
    # 3.读取excel的某一个sheet
    # df = pd.read_excel('Python招聘数据（全）.xlsx', sheet_name='Sheet1')
    print(df)
    # 4.获取列标题
    # print(df.columns)
    # 5.获取列行标题
    # print(df.index)
    # 6.制定打印某一列
    # print(df["工资水平"])
    # 7.描述数据
    # print(df.describe())
    # 8.循环遍历数据

    t1 = time.time()
    country_abbr = [] #记录国家简称的数组
    university_name = [] #记录学校名字的数组
    for indexs in df.index:
        # print('index值为: ',df.loc[indexs].values[0])
        if df.loc[indexs].values[0] not in country_abbr:
            country_abbr.append(df.loc[indexs].values[0])
        university_name.append(df.loc[indexs].values[1])
    t2=time.time()
    print(country_abbr.__len__(), country_abbr)
    print(university_name.__len__(), university_name)
    print(country_abbr.__len__())
    print(university_name.__len__())
    print("使用pandas工具包遍历数据耗时：%.2f 秒"%(t2-t1))

 
'''Redis数据库操作'''
# @cache_page(60*15)  # 缓存15分钟
def my_view(request):
    value = cache.get('my_key')
    if value is None:
        value = "Some data"  # 这里可以是数据库查询的结果等
        cache.set('my_key', value, 60*15)  # 同时将数据存入缓存，并设置过期时间
    return HttpResponse(value)
 
'''MySQL数据库操作'''
class MyModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

if __name__ == '__main__':
    read_excel()
    
    # python manage.py migrate  # 应用所有迁移文件到MySQL数据库
    # python manage.py runserver  # 启动Django开发服务器
    # pass
