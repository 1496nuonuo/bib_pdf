#!/usr/bin/env python 
# -*- coding:utf-8 -*-
class titlestr:
    # 定义基本属性
    title_var = ''

    # 定义构造方法
    def __init__(self, title_var):
        self.title_var = title_var

    def change_ligature(self):#转换合字
        self.title_var = self.title_var.replace('ﬁ', 'fi')  # 修改合字，否则搜索时搜索不出
        self.title_var = self.title_var.replace('ﬂ', 'fl')  # 修改合字，否则搜索时搜索不出

    def del_nr(self):#删去换行
        self.title_var = self.title_var.replace('\n', ' ').strip()  # 删去换行

    def del_dash(self):#删去由于换行产生的同一字符内的破折号
        import enchant
        import re
        my_dict_list = ['convolutional','permutable']#补充的专有名词
        temp_inside = re.findall('([\s]([\S]*?)-\s([\S]*?):?\s){1}', self.title_var, re.S)  # 找标题内容
        temp_start = re.findall('^(([\S]*?)-\s([\S]*?):?\s){1}', self.title_var, re.S)  # 开头
        temp_end = re.findall('([\s]([\S]*?)-\s([\S]*?)){1}$', self.title_var, re.S)  # 结尾
        d = enchant.Dict("en_US")
        if len(temp_start) != 0:
            if d.check(temp_start[0][1] + temp_start[0][2]) or ((temp_start[0][1] + temp_start[0][2]) in my_dict_list):
                temp3_out = self.title_var.replace(temp_start[0][0], temp_start[0][1] + temp_start[0][2] + ' ')
            else:
                temp3_out = self.title_var.replace(temp_start[0][0], temp_start[0][1] + ' ' + temp_start[0][2] + ' ')
        else:
            temp3_out = self.title_var
        if len(temp_end) != 0:
            if d.check(temp_end[0][1] + temp_end[0][2]) or ((temp_end[0][1] + temp_end[0][2]) in my_dict_list):
                temp4_out = temp3_out.replace(temp_end[0][0], ' ' + temp_end[0][1] + temp_end[0][2])
            else:
                temp4_out = temp3_out.replace(temp_end[0][0], ' ' + temp_end[0][1] + '-' + temp_end[0][2])
        else:
            temp4_out = temp3_out
        temps = temp4_out
        for ind in range(len(temp_inside)):
            if d.check(temp_inside[ind][1] + temp_inside[ind][2]) or ((temp_inside[ind][1] + temp_inside[ind][2]) in my_dict_list):
                temps = temps.replace(temp_inside[ind][0], ' ' + temp_inside[ind][1] + temp_inside[ind][2] + ' ')
            else:
                temps = temps.replace(temp_inside[ind][0], ' ' + temp_inside[ind][1] + '-' + temp_inside[ind][2] + ' ')
        self.title_var=temps
