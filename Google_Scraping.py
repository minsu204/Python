from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from bs4 import BeautifulSoup
import tkinter.ttk as ttk
import urllib
import requests

root = Tk()
root.title("Google News Scraping")

# 뉴스 스크래핑
def googleNewsScrap() :
    try : 
        base_url = "https://news.google.com"
        keyword = str(url_keyword.get())
        keyword = urllib.parse.quote(keyword)   # keyword 를 URL 코드로 변환
        url = base_url + "/search?q=" + keyword + "&hl=ko&gl=KR&ceid=KR%3Ako"
        resp = requests.get(url)
        html_src = resp.text
        soup = BeautifulSoup(html_src, "lxml")
        news_items = soup.select("div[class = 'xrnccd']")
        links = []; titles = []; contents = []; agencies = []; reporting_dates = []; reporting_times = []
        
        limit = int(cmb_scrap.get())
        count = 0
        for news in news_items[:limit] :
            # 뉴스 링크
            link = news.find('a', attrs = {"class" : "VDXfz"}).get('href')
            news_link = base_url + link[1:]
            links.append(news_link)

            # 뉴스 제목
            news_title = news.find('a', attrs = {"class" : "DY5T1d RZIKme"}).getText()
            titles.append(news_title)

            # 뉴스 기사
            news_content = news.find("span", attrs = {"class" : "xBbh9"}).getText()
            contents.append(news_content)

            # 뉴스 기관
            news_agency = news.find("a", attrs = {"class" : "wEwyrc AVN2gc uQIVzc Sksgp"}).getText()
            agencies.append(news_agency)

            # 뉴스 일자 및 시간
            try :
                news_reporting = news.find("time", attrs = {"class" : "WW6dff uQIVzc Sksgp"}).get("datetime").split("T")
                news_reporting_date = news_reporting[0]
                news_reporting_time = news_reporting[1][:-1]
                reporting_dates.append(news_reporting_date)
                reporting_times.append(news_reporting_time)
                count += 1
            except :
                news_reporting_date = "없음"
                news_reporting_time = "없음"
                reporting_dates.append(news_reporting_date)
                reporting_times.append(news_reporting_time)
                count += 1
                continue
        result = {'link' : links, 'title' : titles, 'content' : contents, 'agency' : agencies, 'date' : reporting_dates, 'time' : reporting_times}
        return result, count
    except :
        messagebox.showerror("에러", "에러가 발생하였습니다")

# 텍스트로 저장
def newsTextSave(news, count) :
    file_name = str(save_path.get() + '/' + save_file_name.get() + save_file.get())
    news_list = list(news.values())
    title = ["링크 : ", "제목 : ", "기사 : ", "기관 : ", "일자 : ", "시간 : "]
    limit = int(count)
    try :
        if int(cmb_scrap.get()) == count :
            with open(file_name, 'w', encoding = 'utf8') as save :
                for i in range(0, limit) :
                    for j in range(0, len(news_list)) : 
                        save.write(title[j] + news_list[j][i] + '\n')
                    save.write('\n')
                messagebox.showinfo("알림", "저장이 완료되었습니다")
        else :
            with open(file_name, 'w', encoding = 'utf8') as save :
                save.write("스크랩 가능한 뉴스가 선택하신 스크랩 수보다 적습니다.\n\n")
                for i in range(0, limit) :
                    for j in range(0, len(news_list)) : 
                        save.write(title[j] + news_list[j][i] + '\n')
                    save.write('\n')
                messagebox.showinfo("알림", "저장이 완료되었습니다")
    except :
        messagebox.showerror("에러1", "에러가 발생하였습니다")
        return

# 저장경로
def destPath() :
    folder_select = filedialog.askdirectory()
    if folder_select == None :
        return 
    save_path.delete(0, END)
    save_path.insert(0, folder_select)

# 시작 
def start() :
    # 검색어 입력 확인
    if len(url_keyword.get()) == 0 :
        messagebox.showwarning("경고", "검색어를 입력하세요")
        return

    # 저장경로 입력 확인
    if len(save_path.get()) == 0 :
        messagebox.showwarning("경고", "저장경로를 선택하세요")
        return
    
    # 파일명 입력 확인
    if len(save_file_name.get()) == 0 :
        messagebox.showwarning("경고", "파일명을 입력하세요")
        return
    
    # 스크래핑
    news, count = googleNewsScrap()
    newsTextSave(news, count)

# 검색 프레임
url_frame = LabelFrame(root, text = "검색")
url_frame.pack(fill = X, padx = 5, pady = 5)

url_label = Label(url_frame, text = "검색어를 입력하세요")
url_label.pack(side = LEFT, padx = 5, pady = 5)

url_keyword = Entry(url_frame)
url_keyword.pack(side = LEFT, fill = X, padx = 5, pady = 5, ipady = 2)

# 저장경로 프레임
save_frame = LabelFrame(root, text = "저장경로")
save_frame.pack(fill = X, padx = 5, pady = 5)

save_path = Entry(save_frame)
save_path.pack(side = LEFT, fill = X, padx = 5, pady = 5, ipady = 2, expand = True)

btn_save = Button(save_frame, text = "찾아보기", width = 10, command = destPath)
btn_save.pack(side = RIGHT, padx = 5, pady = 5)

# 옵션 프레임
opt_frame = LabelFrame(root, text = "옵션")
opt_frame.pack(fill = X, padx = 5, pady = 5)

# 옵션 - 스크랩 수 
opt_scrap = Label(opt_frame, text = "스크랩 수")
opt_scrap.pack(side = LEFT, fill = X, padx = 5, pady = 5)

scrap_num = ["2", "3", "4", "5"]
cmb_scrap = ttk.Combobox(opt_frame, state = "readonly", values = scrap_num, width = 5)
cmb_scrap.current(0)
cmb_scrap.pack(side = LEFT, padx = 5, pady = 5)

# 옵션 - 저장방식
opt_save = Label(opt_frame, text = "저장방식")
opt_save.pack(side = LEFT, padx = 5, pady = 5)

save_file = Entry(opt_frame, width = 8)
save_file.insert(END, ".txt")
save_file.configure(state = "readonly")
save_file.pack(side = LEFT, padx = 5, pady = 5, ipady = 2)

# 옵션 - 저장파일명
save_name = Label(opt_frame, text = "파일명")
save_name.pack(side = LEFT, padx = 5, pady = 5)

save_file_name = Entry(opt_frame, width = 12)
save_file_name.pack(side = LEFT, padx = 5, pady = 5, ipady = 2)

# 실행 프레임
exec_frame = Frame(root)
exec_frame.pack(fill = X, padx = 5, pady = 5)

btn_close = Button(exec_frame, text = "닫기", width = 10, command = root.quit)
btn_close.pack(side = RIGHT, padx = 5, pady = 5)

btn_start = Button(exec_frame, text = "시작", width = 10, command = start)
btn_start.pack(side = RIGHT, padx = 5, pady = 5)

root.resizable(False, False)
root.mainloop()