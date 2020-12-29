'''
创建 excel 并将采集的关键词写入文件中
'''
import xlwt

# # 将获取到的数据写入excel中
work = xlwt.Workbook(encoding='GBK')
workSheet = work.add_sheet('Sheet')
# 设置表格的标头
workSheet.write(0, 0, '关键词')
workSheet.write(0, 1, '排名')
workSheet.write(0, 2, 'PC搜索量')
excel_line = 1  # 定义excel 的行号

def sava_excel(keywords,index,included):
    '''
    保存挖掘的关键词
    :param keywords:关键词
    :param index:PC移动指数
    :param included:收录量
    :return:
    '''
    global excel_line
    # 开始定入 excel
    workSheet.write(excel_line, 0, keywords)  # 第一列
    workSheet.write(excel_line, 1, index)  # 第二列
    workSheet.write(excel_line, 2, included)  # 第三列
    excel_line = excel_line + 1

    work.save(r'爱站词库.xls')
