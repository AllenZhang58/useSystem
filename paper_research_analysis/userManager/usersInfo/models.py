from django.db import models

# Create your models here.

'''
用户管理需要用到的信息包含:

登录表 login_tab
    用户名 userName varchar(30) not null
    密码 userPass varchar(30) not null
    邮箱 userEmail varchar(30) not null
    Google关联
    个人信息表(外键ID) userinfo_id int
    操作档案表(外键ID) int
    会员等级表(外键ID) ulevel_id int
    用户状态表(外键ID) ustatus_id int

个人信息表 users_info  (1对1,一个用户账号对应一条个人信息表数据)
    姓名 realName varchar(50)
    年龄 age int not null defoult 18
    性别 gender enum('Male', 'Female', 'Confidential') not null defoult 3
    出生日期 birth_date datetime
    职位(外键ID) position_id int
    学校(外键ID) university_id int

职位表 position_tab (字典表)
    职位名称 position_name varchar(10)

国家表 nation_tab (字典表)
    国家简称 country_abbr varchar(5)

学校表 university_tab (字典表)
    学校名称 university_name varchar(100)
    学校网址 university_web varchar(100)
    所在国家(外键ID) nation_id int

会员等级表 user_level (1对多,一个用户账号对应多条会员等级表数据; 等级0只保留最新一条操作数据; 等级1只保留最新三条操作数据; 等级2只保留最新五条操作数据; 
等级3只保留所有操作数据,显示最近十条操作数据; )
    用户等级 levels tinyint (0-未验证用户; 1-邮件验证用户; 2-人员验证用户; 3-付费用户)
    缴费编号(外键ID) pay_id int
    等级有效期 validity_period datetime (等级为0/1/2均为无限时间[null]; 等级为3-1为1天有效期; 等级为3-2为1周有效期; 等级为3-3为1月有效期; 等级为3-4为6月有效期;
    等级为3-5为1年有效期; 等级为3-6为终身有效期;[为空或时间精确到日,与缴费记录表中的缴费时间对应])

缴费记录表 pay_tab (1对多,一个用户账号对应多条缴费记录表数据)
    缴费金额 pay_money decimal(5,2)
    缴费时间 pay_time datetime
    缴费银行名 pay_bank_name varchar(50)
    缴费银行账号 pay_bank_id varchar(50)
    ...(待定)

用户状态表 user_status (1对1,一个用户账号对应一条用户状态表数据)
    验证状态(邮箱验证;0-未验证;1-已验证) email_verify_state bool default 0
    验证时间(邮箱验证) email_verify_time datetime default null
    验证状态(教师/学生验证-老师验证学生, 学生不能验证学生) person_verify_state tinyint (0-未验证;1-一人已验证;2-两人已验证;3-三人已验证)
    验证时间(n个人员验证的具体时间-精确到分钟) person_verify_time varchar(200) default null (保存多个datetime时间,每个时间精确到时分秒即可,以逗号隔开)
    验证人员(默认不少于3人的验证,关联3个人id的数组) person_verify_id varchar(100) (保存多个系统用户ID值,每个ID值用逗号隔开)
    活跃状态(1-每天至少访问1次-活跃常驻;2-每周至少访问不少于2次-活跃;3-偶有访问;4-一个月以上没有访问过-沉寂用户;5-一年以上没有访问过-沉寂注销用户) active_state tinyint
    活跃时间(上次活跃/登录时间) active_time datetime (精确到时分秒即可)
    活跃时长(离线时间-登录时间;单位分钟,不满1分钟的按1分钟计算) active_duration varchar(100)
    注销状态(0-使用中;1-不再使用-主动废弃;2-沉寂用户-一年没用系统自动变更状态;该状态用户登陆后无法正常使用,需再次走验证流程)  logout_state tinyint default 0
    注销时间(状态变为注销的时间-精准到分钟) logout_time datetime default null

操作档案表 Operation_record (1对多,一个用户账号对应多条操作档案表数据)
    使用时间 usage_time datetime(提交idea开始与AI交互时间)
    检索条件ID search_id varchar(100)(与AI沟通的起因记录)
    报告内容 record_info varchar(100) (与AI沟通过程记录;生成的表单和视图)
    公开状态 open_state bool default 1(0-公开;1-私有)
    存档来源 operation_for varchar(10)(AI交互;图表;)
'''

'''职位字典表'''
class position_tab(models.Model):
    position_name = models.CharField(max_length=10) #职位名称
    
    def __str__(self) -> str:
        return self.position_name

'''国家字典表'''
class nation_tab(models.Model): 
    country_abbr = models.CharField(max_length=3) #国家简称

    def __str__(self) -> str:
        return self.country_abbr

'''学校字典表'''
class university_tab(models.Model): 
    university_name  = models.CharField(max_length=100) #学校名称
    university_web = models.CharField(max_length=200) #学校网址
    nation_id = models.ForeignKey(nation_tab, on_delete=models.CASCADE) # 所在国家(外键ID)
    
    def __str__(self) -> str:
        return self.university_name, self.university_web, self.nation_id

'''个人信息表(用户补充表)'''
class users_info(models.Model): #  (1对1,一个用户账号对应一条个人信息表数据)
    realName = models.CharField(max_length=50) #姓名
    age = models.IntegerField(default=18) #年龄
    gender = models.IntegerField(default=3) #性别 enum('Male', 'Female', 'Confidential')
    birth_date = models.DateTimeField() #出生日期
    position_id = models.ForeignKey(position_tab, on_delete=models.CASCADE) #职位(外键ID) 
    university_id = models.ForeignKey(university_tab, on_delete=models.CASCADE) #学校(外键ID)

    def __str__(self) -> str:
        return self.realName, self.age, self.gender, self.birth_date, self.position_id, self.university_id

'''缴费记录表 (1对1,一次会员缴费记录对应一条会员等级表中一条数据记录)'''
class pay_tab(models.Model):
    pay_money = models.models.DecimalField(max_digits=5, decimal_places=2) #缴费金额 decimal(5,2)
    pay_time = models.DateTimeField() #缴费时间 datetime
    pay_bank_name = models.CharField(max_length=50) #缴费银行名 varchar(50)
    pay_bank_id = models.CharField(max_length=50) #缴费银行账号 varchar(50)
    # ...(待定)

    def __str__(self) -> str:
        return self.pay_money, self.pay_time, self.pay_bank_name, self.pay_bank_id

'''会员等级表 (1对多,一个用户账号对应多条会员等级表数据; 等级0只保留最新一条操作数据; 等级1只保留最新三条操作数据; 等级2只保留最新五条操作数据; 等级3只保留所有操作数据,显示最近十条操作数据; )'''
class user_level(models.Model):
    levels = models.SmallIntegerField() #用户等级 tinyint (0-未验证用户; 1-邮件验证用户; 2-人员验证用户; 3-付费用户) 
    pay_state = models.SmallIntegerField() #付费状态(0-待付费; 1-已付费[付费功能后状态变更为已付费,会员等级变更为已付费状态]; 2-未付费[待付费状态24小时后仍未付费,则状态系统自动变更为未付费;同时此条数据逻辑删除])
    state_change_time = models.DateTimeField() #付费状态变更为待付费时的时间, 状态变更为未付费的24小时逻辑依据来源
    pay_id = models.ForeignKey(pay_tab, on_delete=models.CASCADE) #缴费编号(外键ID)  int
    validity_period = models.DateTimeField() #等级有效期 datetime (等级为0/1/2均为无限时间[null]; 等级为3-1为1天有效期; 等级为3-2为1周有效期; 等级为3-3为1月有效期; 等级为3-4为6月有效期;等级为3-5为1年有效期; 等级为3-6为终身有效期;[为空或时间精确到日,与缴费记录表中的缴费时间对应])
    is_validity = models.BooleanField(default=0) #当前数据是否逻辑删除,如果当前数据用户等级状态为(0-未删除;1-已删除)

    def __str__(self) -> str:
        return self.levels, self.pay_id, self.validity_period

'''用户状态表 (1对1,一个用户账号对应一条用户状态表数据)''' 
class user_status(models.Model): 
    email_verify_state = models.BooleanField(default=False) #验证状态(邮箱验证;false-未验证;true-已验证) bool default false
    email_verify_time = models.DateTimeField(default=None)#验证时间(邮箱验证) datetime default none
    person_verify_state = models.SmallIntegerField(default=0) #验证状态(教师/学生验证-老师验证学生, 学生不能验证学生) tinyint (0-未验证;1-一人已验证;2-两人已验证;3-三人已验证)
    person_verify_time = models.CharField(max_length=200, default=None) #验证时间(n个人员验证的具体时间-精确到分钟) varchar(200) default none (保存多个datetime时间,每个时间精确到时分秒即可,以逗号隔开)
    person_verify_id = models.CharField(max_length=100, default=None)#验证人员(默认不少于3人的验证,关联3个人id的数组) varchar(100) (保存多个系统用户ID值,每个ID值用逗号隔开)
    active_state = models.SmallIntegerField(default=0) #活跃状态(0-新用户,使用未超过1个月的用户,超出一个月后计算活跃度,改变活跃值;1-每天至少访问1次-活跃常驻;2-每周至少访问不少于2次-活跃;3-偶有访问;4-一个月以上没有访问过-沉寂用户;5-一年以上没有访问过-沉寂注销用户) tinyint
    active_time =models.DateTimeField()#活跃时间(上次活跃/登录时间) datetime (精确到时分秒即可)
    active_duration = models.CharField(max_length=100,default=None)#活跃时长(离线时间-登录时间;单位分钟,不满1分钟的按1分钟计算) varchar(100)
    logout_state = models.SmallIntegerField(default=0) #注销状态(0-使用中;1-不再使用-主动废弃;2-沉寂用户-一年没用系统自动变更状态;该状态用户登陆后无法正常使用,需再次走验证流程) tinyint default 0
    logout_time = models.DateTimeField(default=None) #注销时间(状态变为注销的时间-精准到分钟) datetime default none

    def __str__(self) -> str:
        return self.email_verify_state, self.email_verify_time, self.person_verify_state, self.person_verify_time, self.person_verify_id, self.active_state, self.active_time, self.active_duration, self.logout_state, self.logout_time

'''操作档案表 (1对多,一个用户账号对应多条操作档案表数据)'''
class Operation_record(models.Model):
    usage_time = models.DateTimeField() #使用时间 datetime(提交idea开始与AI交互时间)
    search_id = models.CharField(max_length=100) #检索条件ID varchar(100)(与AI沟通的起因记录)
    record_info = models.CharField(max_length=100) #报告内容 varchar(100) (与AI沟通过程记录;生成的表单和视图)
    open_state = models.BooleanField(default=False) #公开状态 bool default false(true-公开;false-私有)
    operation_for = models.CharField(max_length=10) #存档来源 varchar(10)(AI交互;图表;)

    def __str__(self) -> str:
        return self.usage_time, self.search_id, self.record_info, self.open_state, self.operation_for

'''登录表(用户基础表)'''
class login_tab(models.Model):
    userName = models.CharField(max_length=30) #用户名
    userPass = models.CharField(max_length=30) #密码
    userEmail = models.CharField(max_length=50) #邮箱
    userinfo_id = models.ForeignKey(users_info, on_delete=models.CASCADE) #个人信息表(外键ID)
    ulevel_id = models.ForeignKey(user_level, on_delete=models.CASCADE) #会员等级表(外键ID) int
    ustatus_id = models.ForeignKey(user_status, on_delete=models.CASCADE) #用户状态表(外键ID) int
    operation_id  = models.ForeignKey(Operation_record, on_delete=models.CASCADE)#操作档案表(外键ID) int

    def __str__(self) -> str:
        return self.userName, self.userPass, self.userEmail, self.userinfo_id
