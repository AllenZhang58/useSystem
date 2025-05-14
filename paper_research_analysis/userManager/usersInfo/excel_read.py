import pandas as pd
from pathlib import Path
import time

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
    cu_dict = {}
    str_sql= ''
    f = open('sql_info.txt', 'w', encoding = 'utf-8')  #写文件使用

    for indexs in df.index:
        # print('index值为: ',df.loc[indexs].values[2])
        # country_abbr.append(df.loc[indexs].values[0])
        # university_name.append(df.loc[indexs].values[1])
        str_info = df.loc[indexs].values[1] + ';' + df.loc[indexs].values[2]
        cu_dict.update({str(df.loc[indexs].values[0]) : str_info})
        str_sql = f'insert into usersinfo_university_tab(university_name, university_web, nation_id_id) select "{df.loc[indexs].values[1]}", "{df.loc[indexs].values[2]}",  id from usersinfo_nation_tab where country_abbr = "{df.loc[indexs].values[0]}";' 
        print(str_sql)
        buf = f.write(f'{str_sql} \n')
    f.close()
    t2=time.time()
    # print(country_abbr.__len__(), country_abbr)
    # print(cu_dict.__len__(), cu_dict)
    # print(country_abbr.__len__())
    # print(university_name.__len__())
    print("使用pandas工具包遍历数据耗时：%.2f 秒"%(t2-t1))

if __name__ == '__main__':
    read_excel()
 