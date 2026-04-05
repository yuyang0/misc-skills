#!/usr/bin/env python3
"""
Sina Finance News Crawler Skill
爬取新浪财经个股新闻列表，支持美股、港股、A股
"""

import html
import time
import json
import re
import random
from typing import List, Dict, Optional

from scrapling.fetchers import FetcherSession
from scrapling.parser import Adaptor


class SinaFinanceNewsCrawler:
    """新浪财经新闻爬虫"""

    def __init__(self, delay: float = 1.0):
        """
        初始化爬虫

        Args:
            delay: 请求间隔时间（秒），用于反爬控制，默认1秒
        """
        self.delay = delay
        self._session_manager = FetcherSession(
            timeout=15,
            retries=2,
            headers={'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'},
        )
        self._session = None
        self.last_request_time = 0

    def __enter__(self):
        self._session = self._session_manager.__enter__()
        return self

    def __exit__(self, *args):
        self._session_manager.__exit__(*args)
        self._session = None

    def _get_session(self):
        """获取 session，如果未在 with 块中使用则自动创建临时 session"""
        if self._session is not None:
            return self._session
        self._session_manager._client = None
        self._session_manager._is_alive = False
        self._session = self._session_manager.__enter__()
        return self._session

    def _rate_limit(self):
        """
        频率控制，加入随机延迟避免固定模式

        实际延迟时间为 delay ± 20% 的随机值，更接近真实用户行为
        """
        current_time = time.time()
        elapsed = current_time - self.last_request_time

        # 在基础延迟上加入 ±20% 的随机波动
        random_factor = random.uniform(0.8, 1.2)
        actual_delay = self.delay * random_factor

        if elapsed < actual_delay:
            time.sleep(actual_delay - elapsed)
        self.last_request_time = time.time()

    def _parse_stock_code(self, stock_code: str) -> tuple:
        """
        解析股票代码，将用户输入转换为新浪财经的格式

        同时支持前缀格式（SH.600519）和后缀格式（600519.SH）。
        """
        parts = stock_code.upper().split('.')
        if len(parts) != 2:
            raise ValueError(f"股票代码格式错误: {stock_code}，正确格式如 HK.00700, US.AAPL, SH.600519")

        market, code = parts

        # 兼容后缀格式，如 600519.SH -> SH.600519
        valid_markets = {'HK', 'US', 'SH', 'SZ'}
        if market not in valid_markets and code in valid_markets:
            market, code = code, market

        if market == 'HK':
            return 'hk', code
        elif market == 'US':
            return 'us', code.upper()
        elif market == 'SH':
            return 'sh', code
        elif market == 'SZ':
            return 'sz', code
        else:
            raise ValueError(f"不支持的市场类型: {market}，支持 HK/US/SH/SZ")

    def _build_news_url(self, market_type: str, code: str) -> str:
        """
        根据市场类型构建新闻页面URL

        URL格式：
            - 港股: https://stock.finance.sina.com.cn/hkstock/news/00700.html
            - 美股: https://biz.finance.sina.com.cn/usstock/usstock_news.php?symbol=NVDA
            - A股(沪): https://vip.stock.finance.sina.com.cn/corp/go.php/vCB_AllNewsStock/symbol/sh600519.phtml
        """
        if market_type == 'hk':
            return f"https://stock.finance.sina.com.cn/hkstock/news/{code}.html"
        elif market_type == 'us':
            return f"https://biz.finance.sina.com.cn/usstock/usstock_news.php?symbol={code}"
        elif market_type in ('sh', 'sz'):
            return f"https://vip.stock.finance.sina.com.cn/corp/go.php/vCB_AllNewsStock/symbol/{market_type}{code}.phtml"
        else:
            raise ValueError(f"不支持的市场类型: {market_type}")

    def _fetch(self, url: str) -> Optional[Adaptor]:
        """
        发起 GET 请求，返回 scrapling Response（同时是 Adaptor）。

        scrapling 基于 Content-Type 头判断编码，对部分新浪页面会误判为 utf-8，
        实际编码在 HTML <meta charset> 中声明为 gbk。这里从原始字节中提取
        meta charset，若与检测结果不同则用正确编码重新构建 Adaptor。
        """
        try:
            self._rate_limit()
            session = self._get_session()
            resp = session.get(url)
            if resp.status != 200:
                return None

            # 从原始字节中提取 HTML 声明的编码
            head_ascii = resp._raw_body[:2000].decode('ascii', errors='ignore')
            m = re.search(r'charset=["\']?([a-zA-Z0-9_-]+)', head_ascii, re.IGNORECASE)
            declared_enc = m.group(1).lower() if m else None

            # scrapling 误判时用正确编码重新解析
            if declared_enc and declared_enc not in ('utf-8', 'utf8') and resp.encoding.lower() in ('utf-8', 'utf8'):
                html_text = resp._raw_body.decode(declared_enc, errors='replace')
                return Adaptor(html_text, url=url)

            return resp
        except Exception as e:
            return None

    def _parse_hk_news(self, resp: Adaptor) -> List[Dict]:
        """
        解析港股新闻页面

        页面结构：
            <ul class="list01" id="js_ggzx">
              <li><a href="URL" target="_blank">标题</a> <span class="rt">2026-04-05 15:36:00</span></li>
            </ul>
        """
        news_list = []
        ul = resp.css('ul.list01')
        if not ul:
            return news_list

        for li in ul[0].css('li'):
            a = li.css('a')
            span = li.css('span.rt')
            if not a or not span:
                continue

            title = a[0].text.strip()
            url = a[0].attrib.get('href', '').strip()
            pub_time = span[0].text.strip()

            if not title or not url:
                continue

            if url.startswith('//'):
                url = 'https:' + url
            elif url.startswith('/'):
                url = 'https://stock.finance.sina.com.cn' + url

            news_list.append({'title': title, 'time': pub_time, 'url': url})

        return news_list

    def _parse_us_news(self, resp: Adaptor) -> List[Dict]:
        """
        解析美股新闻页面

        页面结构：
            <ul class="xb_list">
              <li>
                <span class="xb_list_r">来源 | 2026年04月05日 15:52</span>
                <a href="URL">标题</a>
              </li>
            </ul>
        """
        news_list = []
        ul = resp.css('ul.xb_list')
        if not ul:
            return news_list

        for li in ul[0].css('li'):
            a = li.css('a')
            span = li.css('span.xb_list_r')
            if not a:
                continue

            title = a[0].text.strip()
            url = a[0].attrib.get('href', '').strip()
            if not title or not url:
                continue

            # 从 span 提取时间："来源 | 2026年04月05日 15:52"
            pub_time = ''
            if span:
                m = re.search(r'(\d{4})年(\d{2})月(\d{2})日\s+(\d{2}:\d{2})', span[0].text)
                if m:
                    pub_time = f"{m.group(1)}-{m.group(2)}-{m.group(3)} {m.group(4)}"

            if url.startswith('//'):
                url = 'https:' + url
            elif url.startswith('/'):
                url = 'https://biz.finance.sina.com.cn' + url

            news_list.append({'title': title, 'time': pub_time, 'url': url})

        return news_list

    def _parse_ashare_news(self, resp: Adaptor) -> List[Dict]:
        """
        解析A股新闻页面

        页面结构（html_content 中 &nbsp; 序列化为 &#160;，unescape 后为 \\xa0）：
            <div class="datelist"><ul>
              \\xa0\\xa0\\xa0\\xa02026-04-05\\xa011:41\\xa0\\xa0<a href="URL">标题</a> <br>
            </ul></div>
        """
        news_list = []
        dl = resp.css('.datelist')
        if not dl:
            return news_list

        inner = html.unescape(dl[0].html_content or '')

        # &#160; 经 unescape 后变为 \xa0，用 [\s\xa0]+ 同时兼容普通空格和 non-breaking space
        pattern = r'(\d{4}-\d{2}-\d{2})[\s\xa0]+(\d{2}:\d{2})[\s\xa0]+<a[^>]*href=[\'"]([^\'"]+)[\'"][^>]*>([^<]+)</a>'
        for date, t, url, title in re.findall(pattern, inner):
            title = title.strip()
            url = url.strip()
            if not title or not url:
                continue
            if url.startswith('//'):
                url = 'https:' + url
            elif url.startswith('/'):
                url = 'https://vip.stock.finance.sina.com.cn' + url
            news_list.append({'title': title, 'time': f'{date} {t}', 'url': url})

        return news_list

    def _scrape_news_page(self, market_type: str, code: str, max_news: int) -> List[Dict]:
        """爬取第一页新闻，截取至 max_news 条"""
        url = self._build_news_url(market_type, code)

        resp = self._fetch(url)
        if resp is None:
            return []

        if market_type == 'hk':
            news_list = self._parse_hk_news(resp)
        elif market_type == 'us':
            news_list = self._parse_us_news(resp)
        else:  # sh / sz
            news_list = self._parse_ashare_news(resp)

        return news_list[:max_news]

    def get_stock_news(self, stock_code: str, max_news: int = 20) -> List[Dict]:
        """
        获取指定股票的新闻列表

        Args:
            stock_code: 股票代码，支持前缀（SH.600519）和后缀（600519.SH）两种格式
            max_news: 最多获取的新闻数量，默认20条（取第一页结果，不翻页）

        Returns:
            新闻列表，每条新闻包含:
                - title: 标题
                - time: 发布时间
                - url: 新闻链接

        Example:
            >>> with SinaFinanceNewsCrawler() as crawler:
            ...     news = crawler.get_stock_news('HK.00700', max_news=10)
            ...     for item in news:
            ...         print(f"{item['time']} - {item['title']}")
        """
        try:
            market_type, code = self._parse_stock_code(stock_code)

            news_list = self._scrape_news_page(market_type, code, max_news)

            # 去重
            seen_titles = set()
            unique_news = []
            for news in news_list:
                if news['title'] and news['title'] not in seen_titles:
                    seen_titles.add(news['title'])
                    unique_news.append(news)

            return unique_news[:max_news]

        except ValueError as e:
            return []
        except Exception as e:
            import traceback
            traceback.print_exc()
            return []

    def get_multiple_stocks_news(self, stock_codes: List[str], max_news: int = 20) -> Dict[str, List[Dict]]:
        """
        批量获取多个股票的新闻列表

        Args:
            stock_codes: 股票代码列表，如 ['HK.00700', 'US.AAPL', 'SH.600519']
            max_news: 每只股票最多获取的新闻数量，默认20条

        Returns:
            字典，key为股票代码，value为该股票的新闻列表

        Example:
            >>> with SinaFinanceNewsCrawler() as crawler:
            ...     all_news = crawler.get_multiple_stocks_news(['HK.00700', 'US.AAPL'])
            ...     for code, news_list in all_news.items():
            ...         print(f"{code}: {len(news_list)} 条新闻")
        """
        result = {}
        total = len(stock_codes)

        for i, stock_code in enumerate(stock_codes, 1):
            result[stock_code] = self.get_stock_news(stock_code, max_news=max_news)

        return result


def main():
    """主函数，用于命令行调用"""
    import argparse

    parser = argparse.ArgumentParser(
        description='新浪财经个股新闻爬虫，支持单个或多个股票代码',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  %(prog)s HK.00700                          # 获取腾讯(港股)的新闻
  %(prog)s US.AAPL                           # 获取苹果(美股)的新闻
  %(prog)s SH.600519                         # 获取贵州茅台(上海A股)的新闻
  %(prog)s HK.00700 US.AAPL SH.600519        # 获取多只股票的新闻
  %(prog)s HK.00700 --max 10                 # 获取最多10条新闻
  %(prog)s HK.00700 --delay 2                # 设置请求间隔为2秒
  %(prog)s HK.00700 --json                   # 以JSON格式输出
        '''
    )

    parser.add_argument('stock_codes', nargs='+',
                        help='股票代码（支持多个），格式如 HK.00700, US.AAPL, SH.600519')
    parser.add_argument('--max', type=int, default=20,
                        help='每只股票最多获取的新闻数量，默认20')
    parser.add_argument('--delay', type=float, default=1.0,
                        help='请求间隔（秒），默认1秒')
    parser.add_argument('--json', action='store_true',
                        help='以JSON格式输出结果')

    args = parser.parse_args()

    with SinaFinanceNewsCrawler(delay=args.delay) as crawler:
        if len(args.stock_codes) == 1:
            stock_code = args.stock_codes[0]
            news_list = crawler.get_stock_news(stock_code, max_news=args.max)

            if args.json:
                print(json.dumps({stock_code: news_list}, ensure_ascii=False, indent=2))
            else:
                if not news_list:
                    print("未获取到新闻")
                else:
                    print(f"\n{'='*80}")
                    print(f"股票代码: {stock_code}")
                    print(f"新闻数量: {len(news_list)}")
                    print(f"{'='*80}\n")
                    for i, news in enumerate(news_list, 1):
                        print(f"[{i}] {news['title']}")
                        print(f"    时间: {news['time']}")
                        print(f"    链接: {news['url']}")
                        print()
        else:
            all_news = crawler.get_multiple_stocks_news(args.stock_codes, max_news=args.max)

            if args.json:
                print(json.dumps(all_news, ensure_ascii=False, indent=2))
            else:
                for stock_code in args.stock_codes:
                    news_list = all_news.get(stock_code, [])
                    print(f"\n{'='*80}")
                    print(f"股票代码: {stock_code}")
                    print(f"新闻数量: {len(news_list)}")
                    print(f"{'='*80}\n")
                    if news_list:
                        for i, news in enumerate(news_list, 1):
                            print(f"[{i}] {news['title']}")
                            print(f"    时间: {news['time']}")
                            print(f"    链接: {news['url']}")
                            print()
                    else:
                        print("未获取到新闻\n")


if __name__ == '__main__':
    main()
