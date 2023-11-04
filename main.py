import requests
from bs4 import BeautifulSoup

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

def gen_url(name:str) -> str:
    processed_name:str = name.replace(" ", "+")

    processed_name = processed_name.lower()
    
    return "https://scholar.google.com/scholar?start=0&q=" + processed_name + "&hl=en-EN&as_sdt=0,5"


if __name__ == '__main__':
    input_literature = input("输入您要搜索的文献:")
    print("您要搜索的文献是:", input_literature)
    literature_url = gen_url(input_literature)
    
    response = requests.get(literature_url, proxies=proxies)
    
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取文献列表
    articles = soup.find_all('div', attrs={'class': 'gs_r gs_or gs_scl'})

    for article in articles:
        # 提取文献详细信息-id
        literature_id = article['data-cid']
        # print("literature_id:", literature_id)
        
        # 文献标题
        title_div = article.find('h3')
        ref_link = title_div.find('a')['href']
        # print("ref_link:", ref_link)
        title = article.find('h3').text
        print("title:", title)
        
        # 作者 -期刊 ...年份 - 网址
        author = article.find('div', attrs={'class': 'gs_a'}).text
        # print("author:", author)
        
        # pdf 地址
        gs_or_ggsm = article.find('div', attrs={'class': 'gs_or_ggsm'})
        if gs_or_ggsm == None:
            pass
        else:
            pdf_link = gs_or_ggsm.find('a')['href']
            data_clk = gs_or_ggsm.find('a')['data-clk']
            # print("pdf_link:", pdf_link)
            # print("data_clk:", data_clk)
    
    
    # 检查响应头中的编码信息
    encoding = response.encoding
    print(encoding)

    # 使用指定编码解码响应内容
    content = response.content.decode(encoding)


    # 检查响应状态码
    if response.status_code == 200:
        # 响应成功，打印响应内容
        with open('literature.html', 'w', encoding=encoding) as file:
            file.write(content)
        print('文件已保存为 literature.html')
    else:
        # 响应不成功，输出错误信息
        print("请求失败，状态码:", response.status_code)