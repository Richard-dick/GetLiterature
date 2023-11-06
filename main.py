import requests
from bs4 import BeautifulSoup
import os
import pandas as pd


proxies = {
    "http": "127.0.0.1:7890",
    "https": "127.0.0.1:7890"
}

def init_literature_dict() -> dict: 
    literature = dict()
    literature['title'] = list()
    literature['authors'] = list()
    literature['year'] = list()
    literature['link'] = list()
    literature['pdf'] = list()
    literature['enw'] = list()
    literature['cite'] = list()
    literature['id'] = list()
    literature['abstract'] = list()
    return literature

def getCite(clk:str):
    cites = clk.split('=')
    return cites[-2][:-3]

def deal_articles(articles) -> dict:
    art_info_dict = init_literature_dict()
    for article in articles:
        # 提取文献详细信息-id
        art_info_dict['id'].append(article['data-cid'])
        # 处理标题
        title_div = article.find('h3')
        data_clk = title_div.find('a')['data-clk']
        art_info_dict['cite'].append(getCite(data_clk))
        art_info_dict['link'].append(title_div.find('a')['href'])
        art_info_dict['title'].append(article.find('h3').text)
     
        
        # 作者 -期刊 ...年份 - 网址
        author_div = article.find('div', attrs={'class': 'gs_a'}).text
        tmp = deal_author(author_div)
        art_info_dict['authors'].append(tmp[0])
        art_info_dict['year'].append(tmp[2])
        
        # pdf 地址
        pdf_info = article.find('div', attrs={'class': 'gs_or_ggsm'})
        if pdf_info == None:
            art_info_dict['pdf'].append('')
        else:
            art_info_dict['pdf'].append(pdf_info.find('a')['href'])
        
        art_info_dict['enw'] = ''
        art_info_dict['abstract'] = ''
        
    return art_info_dict


def deal_author(author_div:str):
    author_div = author_div.replace(u'\xa0','')
    [authors, Jour, pub] = author_div.split('- ')
    _ = Jour.split(',')
    if len(_) == 1:
        journal = "book"
        year = _[0]
    else:
        [journal, year] = Jour.split(',')
    return [authors, journal, year, pub]

def gen_url(name:str) -> str:
    processed_name:str = name.replace(" ", "+")

    processed_name = processed_name.lower()
    
    return "https://scholar.google.com/scholar?start=0&q=" + processed_name + "&hl=en-EN&as_sdt=0,5"


if __name__ == '__main__':
    input_literature = input("输入您要搜索的文献:")
    print("您要搜索的文献是:", input_literature)
    dir_name = input_literature.replace(' ','')
    literature_url = gen_url(input_literature)
    
    response = requests.get(literature_url, proxies=proxies)
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取文献列表
    articles = soup.find_all('div', attrs={'class': 'gs_r gs_or gs_scl'})

    article_info = deal_articles(articles)

    # 检查响应头中的编码信息
    encoding = response.encoding
    print(encoding)

    # 使用指定编码解码响应内容
    content = response.content.decode(encoding)

    os.mkdir('./literature/' + dir_name)

    # 创建 DataFrame
    df = pd.DataFrame(article_info)

    # 将数据写入 Excel 文件
    df.to_excel('./literature/' + dir_name + '/info.xlsx', index=True)

    # 检查响应状态码
    if response.status_code == 200:
        # 响应成功，打印响应内容
        with open('./literature/' + dir_name + '/page.html', 'w', encoding=encoding) as file:
            file.write(content)
        print('文件已保存在literature中: ', dir_name)
    else:
        # 响应不成功，输出错误信息
        print("请求失败，状态码:", response.status_code)
        
    # 保存为excel文件