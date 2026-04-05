# Scripts

This directory contains the main crawler script for the Sina Finance News Skill.

## Main Script

### sina_finance_news.py

The core crawler implementation for fetching financial news from Sina Finance.

**Features:**
- Single stock news fetching
- Batch fetching for multiple stocks
- Support for US, HK, and CN A-share markets
- Smart rate limiting with randomization
- Command-line interface
- Python module API

**Command Line Usage:**
```bash
# Run from project root
python scripts/sina_finance_news.py HK.00700

# Or directly
cd scripts
python sina_finance_news.py HK.00700 --max 10
```

**Python Module Usage:**
```python
import sys
sys.path.insert(0, 'scripts')

from sina_finance_news import SinaFinanceNewsCrawler

with SinaFinanceNewsCrawler(delay=1.5) as crawler:
    news = crawler.get_stock_news('HK.00700', max_news=20)
```

## Command Line Options

- `stock_codes`: One or more stock codes (e.g., HK.00700, US.AAPL)
- `--max N`: Maximum news items per stock (default: 20)
- `--delay N`: Request delay in seconds (default: 1.0)
- `--json`: Output results in JSON format

## Examples

```bash
# Single stock
python scripts/sina_finance_news.py HK.00700

# Multiple stocks
python scripts/sina_finance_news.py HK.00700 US.AAPL SH.600519

# Limit results and use JSON output
python scripts/sina_finance_news.py US.NVDA --max 5 --json

# Custom delay for rate limiting
python scripts/sina_finance_news.py HK.00700 --delay 2
```

## Rate Limiting

The crawler implements smart rate limiting:
- Default delay: 1 second between requests
- Adds ±20% random variation to avoid detection patterns
- Recommended for production: 2+ seconds delay

See the main README.md for more detailed usage examples and documentation.
