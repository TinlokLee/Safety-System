# ! /usr/bin/env python
# coding:utf-8
# python interpreter:3.6.6
# author: Lee
import hashlib
import datetime
import shelve
import time
 
 
# 设置登录超时时间
LOGIN_TIME_OUT = 0.60
# 设置临时存储用户“name”和“password”的shelve文件;允许写回
db = shelve.open("user_shelve", writeback=True)
 
# 新用户注册
def register():
    name = None
 
    # 对用户名的合法性进行检验
    while True:
        name = input("register name:").strip()
        if name in db:
            print("Name already exits!Please try again!")
            continue
        elif None == name:
            print("The name cannot be empty!")
            continue
        elif "Q" == name:
            return
        else:
            break
 
    pwd = input("register passwd:").strip()
    # 防止相同pwd的人存储相同的md5
    db[name] = {"passwd": md5_digest(pwd + name), "last_login_time": time.time()}
 
 
# 判断当前用户“是否合法”和“是否超时”
def olduser():
    name = None
    pwd = None
    passwd = None
 
    while True:
        name = input("name:").strip()
        passwd = input("passwd:").strip()
 
        # 判断当前用户“是否注册”
        try:
            pwd = db[name]["passwd"]
            break
        except AttributeError as ae:
            print("\003[1;31;40mUsername '%s' doesn't existed\033[0m" % name)
            break
        except IndexError as ie:
            print("\003[1;31;40mUsername '%s' doesn't existed\033[0m" % name)
            break
 
    # 判断密码摘要是否准确
    if md5_digest(passwd + name) == pwd:
        login_time = time.time()
        last_login_time = db[name]["last_login_time"]
 
        # 判断当前用户是否超过了登录时间
        if login_time - last_login_time < LOGIN_TIME_OUT:
            print("\033[1;31;40mYou already logged in at: <%s>\033[0m" % 
                    datetime.datetime.fromtimestamp(last_login_time).isoformat())
 
        # 更新最近登录时间
        db[name]["last_login_time"] = login_time
        print("\033[1;32;40mwelcome back\033[0m", name)
    else:
        print("\033[1;31;40mlogin incorrect\033[0m")
 
 
# md5摘要传输近来的明文
def md5_digest(message):
    m5 = hashlib.md5()
    m5.update(message.encode(encoding="utf-8"))
    return m5.hexdigest()
 
 
# 主界面
def menu():
    prompt = """
    (N)ew User Login
    (E)xisting User Login
    (Q)uit
    Enter choice: """
 
    # 设置程序退出标志
    flg = False
    while not flg:
        choice = None
        while True:
            try:
                choice = input(prompt).strip()[0].lower()
            # 捕获异常选择直接变成选q退出程序
            except (EOFError, KeyboardInterrupt):
                print("\033[1;31;40m Error！\033[0m")
                return
 
            print("\nYou picked: [%s]" % choice)  # 提示你的选择是什么
            if choice not in "neq":
                print("invalid option, try again")
                continue
            else:
                break
 
        if choice == "q":
            flg = True
        if choice == "n":
            register()
        if choice == "e":
            olduser()
 
    # 操作完成之后关闭文件句柄
    db.close()
 
 
# 测试模块
if "__main__" == __name__:
    menu()