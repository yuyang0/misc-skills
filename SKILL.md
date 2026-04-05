---
name: sina-finance-news
description: Fetch financial news for stocks from Sina Finance (supports US, HK, CN A-shares)
homepage: https://github.com/yuyang0/misc-skills
user-invocable: true
metadata: {"openclaw":{"emoji":"📰","requires":{"bins":["python3"]},"install":[{"id":"pip","kind":"uv","packages":["scrapling[all]>=0.4.0"],"label":"Install Python dependencies (scrapling)"}]}}
---

# Sina Finance News Skill

A skill for fetching financial news for individual stocks from Sina Finance. Supports:
- **US stocks** (e.g., AAPL, NVDA)
- **Hong Kong stocks** (e.g., 00700 for Tencent)
- **China A-shares** (Shanghai/Shenzhen, e.g., 600519, 000001)

## Usage

This skill provides a Python tool to fetch news for one or multiple stock symbols. Stock codes should be in the format `MARKET.CODE`:

- Hong Kong: `HK.00700` (Tencent)
- US: `US.AAPL` (Apple)
- Shanghai A-share: `SH.600519` (Moutai)
- Shenzhen A-share: `SZ.000001` (Ping An Bank)

## Examples

**Fetch news for a single stock:**
```bash
python3 {baseDir}/sina_finance_news.py HK.00700
```

**Fetch news for multiple stocks:**
```bash
python3 {baseDir}/sina_finance_news.py HK.00700 US.AAPL SH.600519 --max 10
```

**Output in JSON format:**
```bash
python3 {baseDir}/sina_finance_news.py HK.00700 --json
```

## Command Line Options

- `stock_codes` (required): One or more stock codes in format `MARKET.CODE`
- `--max`: Maximum news items per stock (default: 20)
- `--delay`: Request delay in seconds for rate limiting (default: 1.0)
- `--json`: Output results in JSON format

## Python API

You can also use this as a Python module:

```python
from sina_finance_news import SinaFinanceNewsCrawler

with SinaFinanceNewsCrawler(delay=1.5) as crawler:
    # Single stock
    news_list = crawler.get_stock_news('HK.00700', max_news=20)

    # Multiple stocks
    all_news = crawler.get_multiple_stocks_news(
        ['HK.00700', 'US.AAPL', 'SH.600519'],
        max_news=10
    )
```

## Data Format

Each news item contains:
- `title`: News headline
- `time`: Publication time (format: YYYY-MM-DD HH:MM)
- `url`: Full URL to the news article

## Rate Limiting

The crawler implements rate limiting to respect Sina Finance servers:
- Default delay: 1 second between requests
- Recommended for production: 2+ seconds
- User-Agent simulation and session persistence included

## Notes

- Data source: Sina Finance (finance.sina.com.cn)
- Web scraping tool: scrapling library
- The tool respects rate limits and includes anti-scraping measures
- Data is for reference only; verify with official sources
- Use responsibly and in compliance with Sina Finance's terms of service

## Installation

Dependencies are automatically installed via the skill metadata. The skill requires:
- Python 3.7+
- `scrapling[all]>=0.4.0`

## Source

The main implementation is in `sina_finance_news.py` in this skill directory.
