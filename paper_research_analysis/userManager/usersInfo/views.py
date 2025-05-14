
from django.shortcuts import render
# pandas用于解析读取excel数据
from django.http import request
from django.views import View
import pandas as pd
from pathlib import Path
import time
# Redis数据库操作引入
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.http import HttpResponse
# MySQL数据库操作引入
from django.db import models

from usersInfo.models import loginTab, operationRecord, nationTab, universityTab

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



def basePage(request, *args, **kwargs):
     context = {
            'title' : 'base',
            'name' : '我是base页面',
            'content' : '大家好,我是内容部分'
        }
     return render(request, template_name='base.html', context=context)

def indexPage(request, *args, **kwargs):
     context = {
            # 'name' : '我是index页面',
            'title' : 'index的title部分',
            'content' : '大家好,我是内容部分',
            'blog.title' : 'blog的title部分',
            'blog.author' : '作者是孙大圣',
            'blog.last_updated_time' : '2025-05-13 12:12:12',
            'blogs_with_type' : '类型是神话',
            'blog.blog_type.pk' : '博客类型是文字pk',
            'blog.blog_type' : '博客类型是你猜',
            'blog.content' : '博客正文部分这在里',
        }
     return render(request, template_name='userManager/index.html', context=context)

def errorPage(request, *args, **kwargs):
     context = {
            'name' : '我是error页面'
        }
     return render(request, template_name='userManager/error.html', context=context)

def loginTop(request, *args, **kwargs):
        from models import loginTab
        # 查询数据表中的全数据
        loginInfos = loginTab.objects.all()
        # 新增数据
        loginTab.objects.create(
             userName = '',
             userPass = '',
             userEmail = '',
        )
        # 修改数据
        loginTab.objects.filter(id='').update(
             userName = '',
             userPass = ''
        )
        # 删除数据
        loginTab.objects.filter(id='').delete()
        # 条件单数据查询
        loginInfo = loginTab.objects.filter(id = '')
        loginInfo = loginTab.objects.get(id = '')
        # 条件查询
        loginInfo = loginTab.objects.filter(userName__contains = '') #数据字段中包含XX值的条件
        loginInfo = loginTab.objects.filter(userName__endswith = '') #数据字段中以XX值结尾的条件
        loginInfo = loginTab.objects.filter(userName__isnull = True) #数据字段中值为空的条件
        loginInfo = loginTab.objects.filter(id__in = [1,3,5]) #数据字段中包含XX数组值的条件
        loginInfo = loginTab.objects.filter(id__gt = 3) #数据字段中大于XX值的条件
        loginInfo = loginTab.objects.filter(id__gte = 3) #数据字段中大于等于XX值的条件
        loginInfo = loginTab.objects.filter(id__lt = 3) #数据字段中小于XX值的条件
        loginInfo = loginTab.objects.filter(id__lte = 3) #数据字段中小于等于XX值的条件
        loginInfo = loginTab.objects.exclude(id = 3) #数据字段中(不等于/不包含)XX值的条件
        loginInfo = loginTab.objects.filter(pub_date__years = 'XXXX') #数据字段中年份为XX年的条件
        loginInfo = loginTab.objects.filter(pub_date__gt = 'XXXX-XX-XX') #数据字段中年份大于XX年XX月XX日的条件

        # 聚合函数; 返回值为字典, key为数据项名__函数名, value值为查询结果
        from django.db.models import Sum, Max, Avg, Count
        loginTab.objects.aggregate(Sum('int类型的数据项名称'))
        loginTab.objects.aggregate(Max('int类型的数据项名称'))
        loginTab.objects.aggregate(Avg('int类型的数据项名称'))
        loginTab.objects.aggregate(Count('int类型的数据项名称'))
        # 排序函数
        loginTab.objects.all().order_by('数据项名称') # 升序排序/由小到大
        loginTab.objects.all().order_by('-数据项名称') # 降序排序/由大到小
        
        '''多表级联/关联查询:''' 
        # 由一对多的关系表结构, 通过'一'表的查询结果, 去查询'多'表的结果集
        nation_tab = nationTab.objects.get(A = '') # 根据条件查询到数据赋值给一个对象
        nation_tab.universitytab_set.all() #根据查询到的对象,使用语法:对象.外键关系表名_set.all()
        # 由多对一的关系表结构, 通过'多'表的查询结果, 去查询'一'表的结果集
        university_tab = universityTab.objects.get(A = '') # 根据条件查询到数据赋值给一个对象
        university_tab.nation_id.country_abbr # 对象中已存在'一'表的对象值,因此只需直接调用即可

        from django.db.models import F
        loginTab.objects.filter(A_gte = F('B')) #单表中数据项A大于等于数据项B的条件

        #单表多条件,条件之间的关系是并且的查询方式
        loginTab.objects.filter(A_gt='X', id_lt='Y') #查询数据项A大于X, 并且 数据项B小于Y的数据
        loginTab.objects.filter(A_gt='X').filter(id_lt='Y') #逻辑同上
        #单表多条件,条件之间的关系是或者的查询方式
        from django.db.models import Q
        loginTab.objects.filter(Q(A_gt='X') | Q(id_lt='Y')) #|代表或,查询数据项A大于X, 或者 数据项B小于Y的数据
        loginTab.objects.filter(Q(A_gt='X') & Q(id_lt='Y')) #&代表且,查询数据项A大于X, 并且 数据项B小于Y的数据
        loginInfo = loginTab.objects.filter(~Q(id = 3)) #~代表非not,数据字段中(不等于/不包含)XX值的条件; 与exclude()用法相同

        context = {
            'title' : 'title is here',
            'content' : '我是谁???',
        }
        return render(request, template_name='usersInfo/login_top.html', context=context)

if __name__ == '__main__':
    read_excel()
    
    # python manage.py migrate  # 应用所有迁移文件到MySQL数据库
    # python manage.py runserver  # 启动Django开发服务器
    # pass
