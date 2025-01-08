from bs4 import BeautifulSoup
import re

class HTMLProcessor:
    @staticmethod
    def process_html(html):
        soup = BeautifulSoup(html, 'html.parser')
        
        # 移除干扰标签
        noise_tags = [
            'script', 'style', 'nav', 'header', 'footer', 'iframe',
            'aside', 'ad', 'advertisement', 'banner', 'menu', 'toolbar',
            'comment', 'pop', 'copyright'
        ]
        for tag in soup(noise_tags):
            tag.decompose()
        
        # 按优先级排序的可能内容标签
        possible_content_selectors = [
            # 常见文章内容标签
            {'tag': 'article'},
            {'tag': 'main'},
            {'class_': 'article'},
            {'class_': 'post'},
            {'class_': 'content'},
            {'class_': 'entry-content'},
            {'class_': 'article-content'},
            {'class_': 'post-content'},
            {'id': 'content'},
            {'id': 'article'},
            {'id': 'main-content'},
            
            # 博客平台特定标签
            {'class_': 'blog-post'},
            {'class_': 'blogpost'},
            {'class_': 'blog-entry'},
            {'class_': 'wordpress-post'},
            
            # 新闻网站特定标签
            {'class_': 'news-article'},
            {'class_': 'news-content'},
            {'itemprop': 'articleBody'},
            
            # 通用内容容器
            {'role': 'main'},
            {'role': 'article'}, 
            {'tag': 'section'},
        ]
        
        # 尝试按优先级查找内容
        main_content = None
        for selector in possible_content_selectors:
            if 'tag' in selector:
                found = soup.find(selector['tag'])
            else:
                found = soup.find(**selector)
            if found:
                main_content = found
                break
                
        # 如果没找到主要内容,尝试查找最长的文本块
        if not main_content:
            paragraphs = soup.find_all('p')
            if paragraphs:
                # 找到包含最多文本的段落的父元素
                max_text_parent = max(
                    (len(p.get_text()) for p in paragraphs)
                )
                for p in paragraphs:
                    if len(p.get_text()) == max_text_parent:
                        main_content = p.parent
                        break
        
        # 提取文本内容
        if main_content:
            # 移除空行并合并相邻文本
            text_blocks = []
            for text in main_content.stripped_strings:
                if len(text.strip()) > 30:  # 过滤太短的行
                    text_blocks.append(text.strip())
            full_text = '\n'.join(text_blocks)
        else:
            # 如果还是没找到,返回body下最长的文本内容
            full_text = soup.body.get_text(separator='\n', strip=True) if soup.body else ''
        
        # 清理文本
        full_text = re.sub(r'\n{3,}', '\n\n', full_text)  # 移除多余空行
        full_text = re.sub(r'[\t ]+', ' ', full_text)     # 规范化空格
        
        return full_text 