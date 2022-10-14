import pdfplumber
import re
from get_bib import download_bib
from title_change import titlestr
def title_processing(mystr):
    mytitle =titlestr(mystr)
    mytitle.change_ligature()
    mytitle.del_nr()
    mytitle.del_dash()
    return mytitle.title_var
def find_title(bib_str):
    "对于引用文献取出标题，作为搜索"
    temp1 = re.findall('[a-z|˘ı]\.(.*?)(\.|\?)[\s+]([^a-z]|arXiv|nature)', bib_str, re.S)  # 找标题内容#arXiv时也要产生截断
    temp2 = temp1[0][0].replace('\n', ' ').strip()  # 删去换行
    title = title_processing(temp2)
    return title

# Press the green button in the gutter to run the script.
def download_fromto(pdf_filename,dirname):
    with pdfplumber.open(
            pdf_filename) as pdf:
        content = ''
        #       #pdf.pages[i] 是读取PDF文档第i+1页
        #         page = pdf.pages[i]
        #         #page.extract_text()函数即读取文本内容，下面这步是去掉文档最下面的页码
        #         page_content = '\n'.join(page.extract_text().split('\n')[:-1])
        #         content = content + page_content
        # print(len(pdf.pages))  #最大页码是len(pdf.pages),range(a,b)表示从a+1页到b页 #pdf.pages[i] 是读取PDF文档第i+1页
        for i in range(len(pdf.pages)-3,len(pdf.pages)):#需要主动修改页数
            page = pdf.pages[i]
            bounding_box_left = (0, 0, pdf.pages[0].width / 2, pdf.pages[0].height)
            page_left = pdf.pages[i].crop(bounding_box_left)
            page_content = '\n'.join(page_left.extract_text(x_tolerance=0.1).split('\n')[:-1])
            # page.extract_text()函数即读取文本内容，下面这步是去掉文档最下面的页码
            #         page_content = ''.join(page.extract_text().split(" ")[:-1])
            if page_content[-1:] != '\n':
                page_content = page_content + '\n'
            content = content + page_content

            bounding_box_right = (pdf.pages[0].width / 2, 0, pdf.pages[0].width, pdf.pages[0].height)
            page_right = pdf.pages[i].crop(bounding_box_right)
            page_content = '\n'.join(page_right.extract_text(x_tolerance=0.1).split('\n')[:-1])
            if page_content[-1:] != '\n':
                page_content = page_content + '\n'
            content = content + page_content
        regex = r'(?<=[Rr]eferences\n).*'
        s = re.findall(regex, content, re.S)  # 找reference之后的内容
        m = re.findall('\](.*?)\[', s[0], re.S)  # 找][之间的内容]
        k = s[0].split(']')  # 取最后一个bib
        m.append(k[-1])
        d = list(map(find_title, m))
        for num in range(len(d)):
            try:
                download_bib(d[num],str(num+1),dirname)
            except:
                print(dirname+'/'+str(num+1)+".bib"+" can't be to download ")
                print(str(d[num]))
        with open(dirname + '/' + "bib_list.txt", "w", encoding='utf-8') as code:
            code.write(s[0])

