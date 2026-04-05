# 新浪财经个股新闻爬虫 Skill

一个用于爬取新浪财经个股新闻列表的 Python 工具，支持美股、港股、A股。

**可作为 [OpenClaw](https://openclaw.ai/) SKILL 使用！**

## 数据源说明

本工具针对不同市场使用新浪财经的专属新闻页面：

- **港股**：`https://stock.finance.sina.com.cn/hkstock/news/{code}.html`
  - 示例：腾讯(00700) → https://stock.finance.sina.com.cn/hkstock/news/00700.html

- **美股**：`https://biz.finance.sina.com.cn/usstock/usstock_news.php?symbol={code}`
  - 示例：英伟达(NVDA) → https://biz.finance.sina.com.cn/usstock/usstock_news.php?symbol=NVDA

- **A股**：`https://vip.stock.finance.sina.com.cn/corp/go.php/vCB_AllNewsStock/symbol/{market}{code}.phtml`
  - 示例：贵州茅台(sh600519) → https://vip.stock.finance.sina.com.cn/corp/go.php/vCB_AllNewsStock/symbol/sh600519.phtml

## 功能特性

- ✅ 支持多市场股票：美股、港股、上海A股、深圳A股
- ✅ 统一的股票代码格式：市场前缀.股票代码（如 HK.00700）
- ✅ **支持批量查询**：一次性查询多个股票代码
- ✅ 反爬措施：频率控制、User-Agent模拟
- ✅ 完整信息：返回新闻标题、发布时间、URL链接
- ✅ 多种输出格式：文本格式或JSON格式
- ✅ 命令行支持：可直接作为CLI工具使用

## 安装依赖

```bash
pip install -r requirements.txt
```

## 作为 OpenClaw SKILL 使用

### 安装到 OpenClaw

将此项目克隆或复制到 OpenClaw 的 skills 目录：

```bash
# 进入 OpenClaw skills 目录
cd ~/.openclaw/skills

# 克隆此项目
git clone <repository-url> sina-finance-news

# 或者复制整个项目文件夹
cp -r /path/to/misc-skills sina-finance-news
```

### 在 OpenClaw 中使用

安装后，你可以在 OpenClaw 的聊天界面中使用斜杠命令：

```
/sina-finance-news HK.00700
/sina-finance-news US.AAPL --max 10 --json
/sina-finance-news HK.00700 US.AAPL SH.600519
```

或者直接询问 OpenClaw：

```
帮我查一下腾讯(HK.00700)最近的新闻
给我看看苹果、腾讯和茅台的最新新闻
```

OpenClaw 会自动识别并调用此 SKILL 来获取财经新闻。

### SKILL 配置

SKILL 的元数据定义在 `SKILL.md` 文件中，包括：
- 名称：`sina-finance-news`
- 描述：获取新浪财经股票新闻
- 依赖：Python 3 和 scrapling 库
- 支持的市场：美股、港股、A股

---

## 命令行使用（独立使用）

### 股票代码格式

支持的股票代码格式为：`市场前缀.股票代码`

### 支持的市场前缀

| 市场 | 前缀 | 示例 | 说明 |
|------|------|------|------|
| 港股 | HK | HK.00700 | 腾讯控股 |
| 美股 | US | US.AAPL | 苹果公司 |
| 上海A股 | SH | SH.600519 | 贵州茅台 |
| 深圳A股 | SZ | SZ.000001 | 平安银行 |

### 命令行调用示例

#### 单只股票查询

```bash
# 获取腾讯(港股)的新闻
python sina_finance_news.py HK.00700

# 获取苹果(美股)的新闻
python sina_finance_news.py US.AAPL

# 获取贵州茅台(上海A股)的新闻
python sina_finance_news.py SH.600519

# 获取平安银行(深圳A股)的新闻
python sina_finance_news.py SZ.000001
```

#### 多只股票批量查询

```bash
# 查询多只股票（空格分隔）
python sina_finance_news.py HK.00700 US.AAPL SH.600519

# 查询多只港股
python sina_finance_news.py HK.00700 HK.00981 HK.00005

# 查询不同市场的股票
python sina_finance_news.py HK.00700 US.AAPL SH.600519 SZ.000001
```

#### 高级选项

```bash
# 单只股票：获取最多10条新闻
python sina_finance_news.py HK.00700 --max 10

# 多只股票：每只获取5条新闻
python sina_finance_news.py HK.00700 US.AAPL --max 5

# 设置请求间隔为2秒（更安全的反爬策略）
python sina_finance_news.py HK.00700 --delay 2

# 以JSON格式输出
python sina_finance_news.py HK.00700 --json

# 多只股票，JSON格式输出
python sina_finance_news.py HK.00700 US.AAPL SH.600519 --json

# 组合使用
python sina_finance_news.py HK.00700 US.AAPL --max 10 --delay 2 --json
```

### 作为Python模块使用

#### 单只股票查询

```python
from sina_finance_news import SinaFinanceNewsCrawler

# 创建爬虫实例（设置请求间隔为1.5秒）
crawler = SinaFinanceNewsCrawler(delay=1.5)

# 获取腾讯的新闻
news_list = crawler.get_stock_news('HK.00700', max_news=20)

# 处理新闻数据
for news in news_list:
    print(f"标题: {news['title']}")
    print(f"时间: {news['time']}")
    print(f"链接: {news['url']}")
    print("-" * 50)
```

#### 多只股票批量查询

```python
from sina_finance_news import SinaFinanceNewsCrawler

# 创建爬虫实例
crawler = SinaFinanceNewsCrawler(delay=2.0)

# 批量获取多只股票的新闻
stock_codes = ['HK.00700', 'US.AAPL', 'SH.600519', 'SZ.000001']
all_news = crawler.get_multiple_stocks_news(stock_codes, max_news=10)

# 处理结果
for stock_code, news_list in all_news.items():
    print(f"\n{stock_code}: {len(news_list)} 条新闻")
    for news in news_list[:3]:  # 只显示前3条
        print(f"  - {news['title']}")
```

### 高级用法示例

#### 保存多只股票新闻到JSON文件

```python
from sina_finance_news import SinaFinanceNewsCrawler
import json
from datetime import datetime

# 创建爬虫实例
crawler = SinaFinanceNewsCrawler(delay=2.0)  # 2秒间隔，更安全

# 批量获取多只股票的新闻
stocks = ['HK.00700', 'US.AAPL', 'SH.600519', 'SZ.000001']
all_news = crawler.get_multiple_stocks_news(stocks, max_news=20)

# 保存为JSON文件
data = {
    'fetch_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'stocks': all_news
}

with open('stock_news.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n新闻数据已保存到 stock_news.json")
```

#### 根据关键词过滤多只股票的新闻

```python
from sina_finance_news import SinaFinanceNewsCrawler

crawler = SinaFinanceNewsCrawler(delay=1.5)

# 获取多只股票的新闻
stocks = ['HK.00700', 'US.AAPL', 'SH.600519']
all_news = crawler.get_multiple_stocks_news(stocks, max_news=30)

# 过滤包含特定关键词的新闻
keywords = ['财报', '业绩', '营收', '利润']

for stock_code, news_list in all_news.items():
    print(f"\n{stock_code} 包含关键词的新闻:")
    filtered = [n for n in news_list if any(k in n['title'] for k in keywords)]

    for news in filtered:
        print(f"  - {news['title']}")
        print(f"    {news['time']} | {news['url']}")
```

## 返回数据格式

### 单只股票

```python
[
    {
        "title": "新闻标题",
        "time": "2024-01-01 10:30",
        "url": "https://finance.sina.com.cn/..."
    },
    ...
]
```

### 多只股票

```python
{
    "HK.00700": [
        {
            "title": "新闻标题1",
            "time": "2024-01-01 10:30",
            "url": "https://finance.sina.com.cn/..."
        },
        ...
    ],
    "US.AAPL": [
        {
            "title": "新闻标题2",
            "time": "2024-01-01 11:00",
            "url": "https://finance.sina.com.cn/..."
        },
        ...
    ]
}
```

## 反爬措施说明

本工具实施了以下反爬策略：

1. **频率控制**：默认每次请求间隔1秒，可通过 `delay` 参数调整
2. **User-Agent模拟**：模拟真实浏览器访问
3. **会话保持**：使用 `requests.Session` 保持会话，模拟用户行为
4. **请求头设置**：包含 Referer、Accept-Language 等完整请求头

### 建议的使用策略

- 生产环境建议设置 `delay >= 2` 秒
- 避免短时间内大量请求
- 遵守网站的 robots.txt 规则
- 合理使用，不对服务器造成过大压力

## 命令行参数说明

```
usage: sina_finance_news.py [-h] [--max MAX] [--delay DELAY] [--json]
                            stock_codes [stock_codes ...]

positional arguments:
  stock_codes    股票代码（支持多个），格式如 HK.00700, US.AAPL, SH.600519

optional arguments:
  -h, --help     显示帮助信息
  --max MAX      每只股票最多获取的新闻数量，默认20
  --delay DELAY  请求间隔（秒），默认1秒
  --json         以JSON格式输出结果
```

## 错误处理

工具会处理以下常见错误：

- **股票代码格式错误**：会提示正确的格式
- **不支持的市场**：会列出支持的市场类型
- **网络请求失败**：会自动尝试多个数据源
- **解析失败**：会尝试多种解析策略

## 注意事项

1. **数据源变化**：新浪财经的页面结构和API可能会变化，如遇到问题请更新工具
2. **网络环境**：需要能够访问新浪财经网站
3. **编码问题**：新浪财经部分页面使用GBK编码，工具已自动处理
4. **数据准确性**：爬取的数据仅供参考，请以官方数据为准
5. **合法使用**：请遵守相关法律法规，仅用于个人学习研究

## 常见问题

### Q: 为什么获取不到新闻？

A: 可能的原因：
- 股票代码格式错误，请检查格式
- 网络连接问题
- 新浪财经页面结构变化
- 请求频率过高被限制

### Q: 如何提高成功率？

A: 建议：
- 增加请求间隔：`--delay 2` 或更长
- 检查网络连接
- 使用代理（需要自行修改代码添加代理支持）

### Q: 支持实时新闻吗？

A: 工具获取的是新浪财经上已发布的新闻，具有一定延迟。

## 许可证

本工具仅供学习和研究使用。

## 贡献

欢迎提交 Issue 和 Pull Request！
