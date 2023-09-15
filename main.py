import tkinter as tk
from tkinter import *
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
import html2markdown
import os
import platform

# 获取桌面路径
desktop_path = None
if platform.system() == 'Windows':
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
elif platform.system() == 'Darwin':
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
elif platform.system() == 'Linux':
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# 创建文件夹
result_folder_path = os.path.join(desktop_path, "result")
if not os.path.exists (result_folder_path):
    os.makedirs(result_folder_path)

driver = webdriver.Edge()
def login():
    #打开目标网页
    driver.get('https://www.luogu.com.cn')
    #获取网页cookie
    cookies = [{"domain": ".luogu.com.cn", "expiry": 1697333231, "httpOnly": True, "name": "_uid", "path": "/",
                "sameSite": "None", "secure": True, "value": "1093120"},
               {"domain": ".luogu.com.cn", "expiry": 1697333188, "httpOnly": True, "name": "__client_id", "path": "/",
                "sameSite": "None", "secure": True, "value": "c116dc501f33abcbef181cef49752041213090de"}]
    # 循环添加cookie
    for cookie in cookies:
        driver.add_cookie(cookie)

    driver.get('https://www.luogu.com.cn')
    #窗口最小化
    driver.minimize_window()
    #maximize

def find_problem(level,b_page, e_page ):
    level = level.replace('-','−')
    ele1 = []
    ele2 = []
    ele3 = []
    ele4 = []
    element = []
    page = b_page
    # 生成起始网页
    while True:
        i = 1
        url = "https://www.luogu.com.cn/problem/list"
        be_url = url + "?page=" + str(page)
        # 启动网页
        driver.get(be_url)
        element_to_click = driver.find_element(By.CSS_SELECTOR, '#app > div.main-container > main > div > div > div > div.border.table > div.header-wrap > div > div.tag > span > a')
        # 模拟点击该元素
        element_to_click.click()
        common_selector = "#app > div.main-container > main > div > div > div > div.border.table > div.row-wrap > div"
        # 查找题目序号“Pxxxx”
        while True:
            if i == 51:
                break
            selector1 = f"{common_selector}:nth-child({i}) > span:nth-child(2)"     #题号
            selector2 = f"{common_selector}:nth-child({i}) > div.title"             #题目
            selector3 = f"{common_selector}:nth-child({i}) > div.difficulty"        #难度
            selector4 = f"{common_selector}:nth-child({i}) > div.tags"              #算法标签
            i = i+1
            num = driver.find_element(By.CSS_SELECTOR, selector1).text
            title = driver.find_element(By.CSS_SELECTOR, selector2).text
            title = title.replace('/','')
            hard = driver.find_element(By.CSS_SELECTOR, selector3).text
            tag = driver.find_element(By.CSS_SELECTOR, selector4).text
            #筛选条件
            if level != '':
                if hard == level :
                    ele1.append(num)
                    ele2.append(title)
                    ele3.append(hard)
                    ele4.append(tag)
            else :
                ele1.append(num)
                ele2.append(title)
                ele3.append(hard)
                ele4.append(tag)
        page = page + 1
        if page == e_page+1:
            break
    element = list(zip(ele1, ele2, ele3,ele4))
    content = '题目列表信息爬取完毕\n符合条件的题目有：'
    display_text.insert(tk.END, content)
    display_text.insert(tk.END,'\n')
    display_text.update()
    for i in element :
        content = []
        for temp in i:
            temp = ' '.join(temp.split('\n'))
            content.append(temp)
        content = tuple(content)
        display_text.insert(tk.END, content)
        display_text.insert(tk.END,'\n')
        display_text.update()
    content = '开始爬取题目内容：'
    display_text.insert(tk.END, content)
    display_text.insert(tk.END, '\n')
    display_text.update()
    return element

def find_pro_ans(array):
    global desktop_path
    for i in array:
        folder_path = f"{desktop_path}\\result\\{i[0]}-{i[1]}"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        url = 'https://www.luogu.com.cn/problem'
        new_url = url + "/" + i[0]
        # 启动网页
        driver.get(new_url)
        # 查找元素
        result = driver.find_element(By.CSS_SELECTOR, "#app > div.main-container > main > div > section.main > section > div > div:nth-child(2)")
        # 转markdown
        markdown_output = html2markdown.convert(result.text)
        file_name = f"{i[0]}-{i[1]}.md"
        # 构造文件路径
        file_path = f"{folder_path}\\{file_name}"

        # 保存Markdown内容到文件
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(markdown_output)

    content = '题目内容已爬取完！开始爬取题目答案：'
    display_text.insert(tk.END, content)
    display_text.insert(tk.END,'\n')
    display_text.update()

    for i in array:
        url = 'https://www.luogu.com.cn/problem/solution'
        new_url = url + "/" + i[0]
        # 启动网页
        driver.get(new_url)
        # 查找元素
        result = driver.find_element(By.CSS_SELECTOR, "div.marked:first-of-type")
        # 转markdown
        markdown_output = html2markdown.convert(result.text)
        folder_path = f"{desktop_path}\\result\\{i[0]}-{i[1]}"
        file_name = f"{i[0]}-{i[1]}-题解.md"
        # 构造文件路径
        file_path = f"{folder_path }\\{file_name}"

        # 保存Markdown内容到文件
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(markdown_output)

        print("已保存Markdown内容为.md文件到桌面。")

    content = '题目答案已爬取完！'
    display_text.insert(tk.END, content)
    display_text.insert(tk.END,'\n')
    display_text.update()

def crawl():
    level = difficulty_combobox.get()
    b_page = int(start_page_entry.get())
    e_page = int(end_page_entry.get())
    if b_page > e_page:
        display_text.delete("1.0", tk.END)
        display_text.insert(tk.END, "错误：起始页不能大于结束页")
        return

    login()
    problem_data = find_problem(level, b_page, e_page)
    find_pro_ans(problem_data)
    #关闭浏览器
    driver.quit()

root = Tk()

font_style = ("Arial", 12)
bg_color = "lightgray"

# 标签和输入框用于输入起始页和结束页
start_label = tk.Label(root, text="起始页：")
start_label.pack()

start_page_entry = tk.Entry(root, width=10)
start_page_entry.pack()

end_label = tk.Label(root, text="结束页：")
end_label.pack()

end_page_entry = tk.Entry(root, width=10)
end_page_entry.pack()

# 难度选择下拉框
difficulty_label = Label(root, text="难度选择：", font=font_style)
difficulty_label.pack()

selected_difficulty = StringVar()
difficulty_combobox = ttk.Combobox(root, textvariable=selected_difficulty, font=font_style)
difficulty_combobox['values'] = ['入门', '普及-', '普及/提高-', '普及+/提高',
                                 '提高+/省选-', '省选/NOI-','NOI/NOI+/CTSC']  # 设置下拉选项
difficulty_combobox.pack()

# 创建显示内容文本控件
display_text = tk.Text(root, height=20, width=80)
display_text.pack()

# 开始爬取按钮
crawl_button = Button(root, text="爬虫！启动！", command=crawl, font=font_style)
crawl_button.pack()

root.mainloop()
