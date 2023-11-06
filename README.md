# GetLiterature
a tool for getting literature fast


## 获得url

首先通过搜索得到 google scholar 的结果 url.

通过特别的观察, 其结果为:

- https://scholar.google.com/scholar?
- start=...     页数: 0-9是第一页, 以此类推
- 连接符 &
- q=... 后面是查询的字词序列, 用+号相连, 大小写无关
- 连接符 &
- &hl=zh-CN&as_sdt=0,5 不知道什么用, 前面是语言后面是什么 courts, 不懂
- &as_ylo=1999&as_yhi=2000 启示终止年份

如搜索 An artificially generated multiple object auditory space for use where vision is impaired

得到:

https://scholar.google.com/scholar?start=10&q=An+artificially+generated+multiple+object+auditory+space+for+use+where+vision+is+impaired&hl=zh-CN&as_sdt=0,5&as_ylo=1999&as_yhi=1999

所以传入字符串拼接即可, 见函数`gen_url()`

## 解析html文件

现在开始从 html 中获取:
- 文献名称
- 文献作者
- 发表年份
- 地址索引
- pdf地址
- enw地址
- cite号

对文献对应的 div 分析如下:

```html
<div class="gs_r gs_or gs_scl" data-cid="lk0yY1U5lY8J" data-did="lk0yY1U5lY8J" data-lid="" data-aid="lk0yY1U5lY8J" data-rp="0">
    <div class="gs_ggs gs_fl">
        <div class="gs_ggsd">
            <div class="gs_or_ggsm" ontouchstart="gs_evt_dsp(event)" tabindex="-1">
                <a href="http://gtubicomp2014.pbworks.com/w/file/fetch/72893732/gemperle-wearability.pdf" data-clk="hl=zh-CN&amp;sa=T&amp;oi=gga&amp;ct=gga&amp;cd=0&amp;d=10346238757852827030&amp;ei=OBVGZfKKD6KQ6rQP0rSkmAc" data-clk-atid="lk0yY1U5lY8J"> 
                <span class="gs_ctg2">[PDF]</span> pbworks.com</a>
            </div>
        </div>
    </div>
    <div class="gs_ri">
        <h3 class="gs_rt" ontouchstart="gs_evt_dsp(event)">
            <a id="lk0yY1U5lY8J" href="https://ieeexplore.ieee.org/abstract/document/729537/" data-clk="hl=zh-CN&amp;sa=T&amp;ct=res&amp;cd=0&amp;d=10346238757852827030&amp;ei=OBVGZfKKD6KQ6rQP0rSkmAc" data-clk-atid="lk0yY1U5lY8J">
                <b>Design </b>for <b>wearability</b>
            </a>
        </h3>
    <div class="gs_a">F Gemperle, C Kasabach, J Stivoric…&nbsp;- digest of papers&nbsp;…, 1998 - ieeexplore.ieee.org</div>
    <div class="gs_rs">… A product that is wearable should have <b>wear</b><b>ability</b>. This paper explores the concept of <br>dynamic <b>wearability</b> through <b>design</b> research. <b>Wearability</b> is defined as the interaction between …
    </div>
    <div class="gs_fl gs_flb">
        <a href="javascript:void(0)" class="gs_or_sav gs_or_btn" role="button">
            <svg viewBox="0 0 15 16" class="gs_or_svg"><path d="M7.5 11.57l3.824 2.308-1.015-4.35 3.379-2.926-4.45-.378L7.5 2.122 5.761 6.224l-4.449.378 3.379 2.926-1.015 4.35z"></path></svg><span class="gs_or_btn_lbl">保存</span>
        </a> 
        <a href="javascript:void(0)" class="gs_or_cit gs_or_btn gs_nph" role="button" aria-controls="gs_cit" aria-haspopup="true"><svg viewBox="0 0 15 16" class="gs_or_svg"><path d="M6.5 3.5H1.5V8.5H3.75L1.75 12.5H4.75L6.5 9V3.5zM13.5 3.5H8.5V8.5H10.75L8.75 12.5H11.75L13.5 9V3.5z"></path></svg><span>引用</span>
        </a> 
        <a href="/scholar?cites=10346238757852827030&amp;as_sdt=2005&amp;sciodt=0,5&amp;hl=zh-CN&amp;oe=GB">被引用次数：789</a> <a href="/scholar?q=related:lk0yY1U5lY8J:scholar.google.com/&amp;scioq=design+for+wearability&amp;hl=zh-CN&amp;oe=GB&amp;as_sdt=0,5">相关文章</a> 
        <a href="/scholar?cluster=10346238757852827030&amp;hl=zh-CN&amp;oe=GB&amp;as_sdt=0,5" class="gs_nph">所有 28 个版本</a> 
        <a href="javascript:void(0)" title="更多" class="gs_or_mor gs_oph" role="button"><svg viewBox="0 0 15 16" class="gs_or_svg"><path d="M0.75 5.5l2-2L7.25 8l-4.5 4.5-2-2L3.25 8zM7.75 5.5l2-2L14.25 8l-4.5 4.5-2-2L10.25 8z"></path></svg></a> 
        <a href="javascript:void(0)" title="隐藏" class="gs_or_nvi gs_or_mor" role="button"><svg viewBox="0 0 15 16" class="gs_or_svg"><path d="M7.25 5.5l-2-2L0.75 8l4.5 4.5 2-2L4.75 8zM14.25 5.5l-2-2L7.75 8l4.5 4.5 2-2L11.75 8z"></path></svg></a>
    </div>
</div>
</div>

```

得到
- 文献名称--->h3
- 文献作者--->class = gs_a
- 发表年份
- 地址索引
- pdf地址
- enw地址 ----> 还不知道如何处理 javascript:void(0)
- cite号
- 摘要 ---> gs_rs: 但是只有部分截取, 然后即使是同一个网站, 也很难有统一的id和class来寻找abstract, 难绷.

## 难点和未完成的地方

- 一个是摘要如何提取
- 第二个是cite号和具体的作者等还未分离(只需要花时间)
- enw的下载问题
- 多page的寻找问题

构建一个整体的工作流如下:

- 选择查找模式:
  - 关键词搜索文献
    - 输入关键词->生成搜索网页->得到总数量->确定分页数量
    - 对每一页(大概10篇文献), 解析其信息, 存到 dict 中
    - 保存到 excel 中
  - 文献名搜索引用文献
    - 一致
- 其他功能确定:
  - 默认英语
  - 应该有可选年份的空间


## 2023-11-6

cite号分离, author也分离

默认英语

待解决的问题:
- 多网页检索
- cite搜索功能
- 年份选择功能
