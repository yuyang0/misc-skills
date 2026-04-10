---
name: misc
description: 个人杂项工具合集，包含新浪财经个股新闻爬取等功能
homepage: https://github.com/yuyang0/misc-skills
user-invocable: true
metadata: {"openclaw":{"emoji":"🧰","requires":{"bins":["python3"]},"install":[{"id":"pip","kind":"uv","packages":["scrapling[all]>=0.4.0"],"label":"Install Python dependencies (scrapling)"}]}}
---

## 语言规则

根据用户输入的语言自动回复：用户使用英文提问则用英文回复，使用中文提问则用中文回复，其他语言同理。语言不明确时默认使用中文。技术术语（如代码、API 名称、参数名）保持原文不翻译。

## 工具列表

### 新浪财经个股新闻（`scripts/sina_finance_news.py`）

爬取新浪财经的个股新闻，支持美股、港股、A 股（沪深）。

**股票代码格式**：`市场前缀.股票代码`

| 市场 | 前缀 | 示例 |
|------|------|------|
| 港股 | `HK` | `HK.00700`（腾讯） |
| 美股 | `US` | `US.AAPL`（苹果） |
| 上海A股 | `SH` | `SH.600519`（茅台） |
| 深圳A股 | `SZ` | `SZ.000001`（平安银行） |

**命令行调用**：

```bash
# 单只股票
python3 {baseDir}/scripts/sina_finance_news.py HK.00700

# 多只股票
python3 {baseDir}/scripts/sina_finance_news.py HK.00700 US.AAPL SH.600519 --max 10

# JSON 格式输出
python3 {baseDir}/scripts/sina_finance_news.py HK.00700 --json

# 显示详细日志
python3 {baseDir}/scripts/sina_finance_news.py HK.00700 --verbose
```

**命令行参数**：

- `stock_codes`（必填）：一个或多个股票代码
- `--max`：每只股票最多获取的新闻数量（默认 20）
- `--delay`：请求间隔秒数，用于频率控制（默认 1.0）
- `--json`：以 JSON 格式输出
- `--verbose` / `-v`：显示详细日志（INFO 级别）

**Python API**：

```python
import sys
sys.path.insert(0, '{baseDir}/scripts')

from sina_finance_news import SinaFinanceNewsCrawler

with SinaFinanceNewsCrawler(delay=1.5) as crawler:
    # 单只股票
    news_list = crawler.get_stock_news('HK.00700', max_news=20)

    # 多只股票
    all_news = crawler.get_multiple_stocks_news(
        ['HK.00700', 'US.AAPL', 'SH.600519'],
        max_news=10
    )
```

**返回数据格式**：

每条新闻包含：
- `title`：新闻标题
- `time`：发布时间（格式：`YYYY-MM-DD HH:MM`）
- `url`：新闻链接

**说明**：

- 数据来源：新浪财经（finance.sina.com.cn）
- 网页解析：scrapling 库
- 频率控制：默认间隔 1 秒，并加入 ±20% 随机波动避免固定模式
- 数据仅供参考，请以官方数据为准

### 自选股重要新闻分析

自动分析自选股中指定分组的重要新闻，并生成飞书文档报告。

**使用方式**：

当用户说"分析自选股新闻"、"分析XXX分组的新闻"、"查看化妆品分组重要新闻"或类似请求时，执行以下步骤：

1. 获取自选股中指定分组的所有股票
   - 如果用户明确指定分组名称（如"化妆品"、"半导体"），使用该分组
   - 如果用户没有指定分组，默认使用"特别关注"分组
2. 对第一步获取的每一个股票查询个股新闻，请过滤掉距离当前时间超过一周的新闻
3. 分析新闻标题，如果发现对股价可能有重大影响的新闻（比如财报发布、盈利披露或者其他对业务有重大影响的新闻），你需要抓取对应的链接并且对内容生成一个摘要，如果抓取链接的过程出错你可以直接用标题代替
4. 把上一步的结果返回，格式要求是每个股票名称作为一行并且黑体，字体适当增大，接着一条新闻一个段落，把所有内容写入一份飞书文档然后发给我

**使用示例**：

- "分析自选股新闻" → 分析"特别关注"分组
- "分析化妆品分组的新闻" → 分析"化妆品"分组
- "查看半导体板块重要新闻" → 分析"半导体"分组
- "看看新能源分组有什么消息" → 分析"新能源"分组

**说明**：

- 使用 `scripts/sina_finance_news.py` 获取个股新闻
- 自动识别财报、盈利、并购、高管变动等重大新闻
- 新闻时间默认过滤 7 天以前的内容
- 最终输出为格式化的飞书文档
