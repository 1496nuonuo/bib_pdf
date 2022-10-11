import pdfplumber
import re
from get_bib import download_bib
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
def del_pozhehao(mystr):
    import enchant
    import re
    my_dict_list = ['convolutional']
    temp2 = mystr.replace('\n', ' ').strip()  # 删去换行
    temp3 = temp2.replace('ﬁ', 'fi')  # 修改合字，否则搜索时搜索不出
    temp3 = temp3.replace('ﬂ', 'fl')  # 修改合字，否则搜索时搜索不出
    temp1 = re.findall('([\s]([\S]*?)-\s([\S]*?)\s){1}', temp3, re.S)  # 找标题内容
    temp4 = re.findall('^(([\S]*?)-\s([\S]*?)\s){1}', temp3, re.S)   #开头
    temp5 = re.findall('([\s]([\S]*?)-\s([\S]*?)){1}$', temp3, re.S)  #结尾
    d = enchant.Dict("en_US")
    if len(temp4) != 0:
        if d.check(temp4[0][1] + temp4[0][2]) or ((temp4[0][1] + temp4[0][2]) in my_dict_list):
            temp3_out = temp3.replace(temp4[0][0], temp4[0][1] + temp4[0][2] + ' ')
        else:
            temp3_out = temp3.replace(temp4[0][0], temp4[0][1] + ' ' + temp4[0][2] + ' ')
    else:
        temp3_out = temp3
    if len(temp5) != 0:
        if d.check(temp5[0][1] + temp5[0][2]) or ((temp5[0][1] + temp5[0][2]) in my_dict_list):
            temp4_out = temp3_out.replace(temp5[0][0], ' ' + temp5[0][1] + temp5[0][2])
        else:
            temp4_out = temp3_out.replace(temp5[0][0], ' ' + temp5[0][1] + '-' + temp5[0][2])
    else:
        temp4_out = temp3_out
    temps = temp4_out
    for ind in range(len(temp1)):
        if d.check(temp1[ind][1] + temp1[ind][2]) or ((temp1[ind][1] + temp1[ind][2]) in my_dict_list):
            temps = temps.replace(temp1[ind][0], ' ' + temp1[ind][1] + temp1[ind][2] + ' ')
        else:
            temps = temps.replace(temp1[ind][0], ' ' + temp1[ind][1] + '-' + temp1[ind][2] + ' ')
    return temps
def find_title(bib_str):
    "对于引用文献取出标题，作为搜索"
    temp1 = re.findall('[a-z]\.(.*?)(\.|\?)[\s+]([^a-z]|arXiv)', bib_str, re.S)  # 找标题内容
    temp2 = temp1[0][0].replace('\n', ' ').strip()  # 删去换行
    temp3 = temp2.replace('ﬁ', 'fi')  # 修改合字，否则搜索时搜索不出
    title = del_pozhehao(temp3)
    return title

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    with pdfplumber.open(
            r"./Bhardwaj_Efficient_Video_Classification_Using_Fewer_Frames_CVPR_2019_paper.pdf") as pdf:
        content = ''
        #     len(pdf.pages)
        #     for i in range(1):
        #       #pdf.pages[i] 是读取PDF文档第i+1页
        #         page = pdf.pages[i]
        #         #page.extract_text()函数即读取文本内容，下面这步是去掉文档最下面的页码
        #         page_content = '\n'.join(page.extract_text().split('\n')[:-1])
        #         content = content + page_content
        for i in range(len(pdf.pages)-3,len(pdf.pages)):
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
        # print(s[0])
        m = re.findall('\](.*?)\[', s[0], re.S)  # 找][之间的内容]
        k = s[0].split(']')  # 取最后一个bib
        m.append(k[-1])
        d = list(map(find_title, m))
        print(d)
        for num in range(len(d)):
            download_bib(d[num],str(num))
    #     如：s1 = 'Youtube-8m: A large-scale video classiﬁcation benchmark'
    #     s2 = 'Youtube-8m: A large-scale video classification benchmark'

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
