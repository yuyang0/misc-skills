#!/usr/bin/env python3
"""
示例脚本：批量获取多只股票的新闻
"""

from sina_finance_news import SinaFinanceNewsCrawler
import json
from datetime import datetime


def example_single_stock():
    """示例1：获取单只股票的新闻"""
    print("=" * 80)
    print("示例1：获取腾讯控股(HK.00700)的新闻")
    print("=" * 80)

    crawler = SinaFinanceNewsCrawler(delay=1.5)
    news_list = crawler.get_stock_news('HK.00700', max_news=10)

    for i, news in enumerate(news_list, 1):
        print(f"\n[{i}] {news['title']}")
        print(f"    时间: {news['time']}")
        print(f"    链接: {news['url']}")


def example_multiple_stocks():
    """示例2：批量获取多只股票的新闻"""
    print("\n\n" + "=" * 80)
    print("示例2：批量获取多只股票的新闻")
    print("=" * 80)

    # 定义要查询的股票列表
    stocks = ['HK.00700', 'US.AAPL', 'SH.600519', 'SZ.000001']

    crawler = SinaFinanceNewsCrawler(delay=2.0)  # 批量请求时增加间隔

    # 使用批量查询方法
    all_news = crawler.get_multiple_stocks_news(stocks, max_news=5)

    # 显示结果
    for stock_code, news_list in all_news.items():
        print(f"\n{stock_code}: 获取到 {len(news_list)} 条新闻")
        for i, item in enumerate(news_list[:3], 1):
            print(f"  [{i}] {item['title']}")

    return all_news


def example_save_to_file():
    """示例3：保存新闻到JSON文件"""
    print("\n\n" + "=" * 80)
    print("示例3：保存新闻到JSON文件")
    print("=" * 80)

    crawler = SinaFinanceNewsCrawler(delay=1.5)

    # 获取新闻
    stock_code = 'HK.00700'
    news_list = crawler.get_stock_news(stock_code, max_news=20)

    # 准备保存的数据
    data = {
        'stock_code': stock_code,
        'fetch_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'news_count': len(news_list),
        'news': news_list
    }

    # 保存到文件
    filename = f'news_{stock_code.replace(".", "_")}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"新闻数据已保存到文件: {filename}")
    print(f"共保存 {len(news_list)} 条新闻")


def example_filter_by_keyword():
    """示例4：根据关键词过滤多只股票的新闻"""
    print("\n\n" + "=" * 80)
    print("示例4：根据关键词过滤多只股票的新闻")
    print("=" * 80)

    crawler = SinaFinanceNewsCrawler(delay=1.5)

    # 获取多只股票的新闻
    stocks = ['HK.00700', 'US.AAPL', 'SH.600519']
    all_news = crawler.get_multiple_stocks_news(stocks, max_news=30)

    # 过滤包含特定关键词的新闻
    keywords = ['财报', '业绩', '营收', '利润']

    print(f"\n在所有新闻中搜索包含关键词 {keywords} 的新闻:\n")

    for stock_code, news_list in all_news.items():
        filtered_news = [n for n in news_list if any(keyword in n['title'] for keyword in keywords)]

        if filtered_news:
            print(f"\n{stock_code}: 找到 {len(filtered_news)} 条相关新闻")
            for i, news in enumerate(filtered_news[:3], 1):
                print(f"  [{i}] {news['title']}")
                print(f"      时间: {news['time']}")
        else:
            print(f"\n{stock_code}: 未找到包含指定关键词的新闻")


def example_batch_save_to_json():
    """示例5：批量保存多只股票新闻到JSON文件"""
    print("\n\n" + "=" * 80)
    print("示例5：批量保存多只股票新闻到JSON文件")
    print("=" * 80)

    crawler = SinaFinanceNewsCrawler(delay=2.0)

    # 批量获取多只股票的新闻
    stocks = ['HK.00700', 'US.AAPL', 'SH.600519']
    all_news = crawler.get_multiple_stocks_news(stocks, max_news=20)

    # 准备保存的数据
    data = {
        'fetch_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_stocks': len(stocks),
        'stocks': all_news
    }

    # 保存到文件
    filename = f'batch_news_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n批量新闻数据已保存到文件: {filename}")
    total_news = sum(len(news) for news in all_news.values())
    print(f"共保存 {len(stocks)} 只股票的 {total_news} 条新闻")


def main():
    """运行所有示例"""
    print("\n新浪财经新闻爬虫 - 使用示例\n")

    try:
        # 示例1：单只股票
        example_single_stock()

        # 示例2：多只股票批量查询
        example_multiple_stocks()

        # 示例3：保存到文件
        example_save_to_file()

        # 示例4：关键词过滤（多只股票）
        example_filter_by_keyword()

        # 示例5：批量保存到JSON
        example_batch_save_to_json()

        print("\n\n" + "=" * 80)
        print("所有示例运行完成！")
        print("=" * 80)

    except KeyboardInterrupt:
        print("\n\n用户中断执行")
    except Exception as e:
        print(f"\n\n运行出错: {e}")


if __name__ == '__main__':
    main()
