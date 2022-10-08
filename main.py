import pdfplumber
import re
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
def find_title(bib_str):
    "对于引用文献取出标题，作为搜索"
    temp1 = re.findall('[a-z]\.(.*?)[\.\?][\s+][^a-z]', bib_str, re.S)  # 找标题内容
    temp2 = temp1[0].replace('\n', ' ').strip()  # 删去换行
    title = temp2.replace('ﬁ', 'fi')  # 修改合字，否则搜索时搜索不出
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
        for i in range(7, len(pdf.pages)):
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
        print(s[0])
        m = re.findall('\](.*?)\[', s[0], re.S)  # 找][之间的内容]
        k = s[0].split(']')  # 取最后一个bib
        m.append(k[-1])
        d = list(map(find_title, m))
    #     如：s1 = 'Youtube-8m: A large-scale video classiﬁcation benchmark'
    #     s2 = 'Youtube-8m: A large-scale video classification benchmark'

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
