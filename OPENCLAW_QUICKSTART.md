# OpenClaw SKILL - Quick Start Guide

This guide will help you quickly install and use the Sina Finance News skill with OpenClaw.

## What is this?

A financial news crawler skill for OpenClaw that fetches stock news from Sina Finance. Supports:
- 🇺🇸 US stocks (AAPL, NVDA, etc.)
- 🇭🇰 Hong Kong stocks (00700, 00981, etc.)
- 🇨🇳 China A-shares (600519, 000001, etc.)

## Installation

### 1. Clone to OpenClaw skills directory

```bash
cd ~/.openclaw/skills
git clone <repository-url> sina-finance-news
```

Or copy the entire folder:

```bash
cp -r /path/to/misc-skills ~/.openclaw/skills/sina-finance-news
```

### 2. Dependencies (automatic)

OpenClaw will automatically install `scrapling` when you first use this skill.

### 3. Verify installation

Restart OpenClaw or reload skills. You should see `sina-finance-news` in your available skills.

## Usage in OpenClaw

### Via slash command

```
/sina-finance-news HK.00700
/sina-finance-news US.AAPL --max 10
/sina-finance-news HK.00700 US.AAPL SH.600519
```

### Via natural language

```
帮我查一下腾讯(HK.00700)最近的新闻
给我看看苹果、特斯拉和英伟达的最新财经新闻
查询茅台(SH.600519)的新闻，最多10条
```

OpenClaw will automatically recognize your request and invoke this skill.

## Stock Code Format

Use format: `MARKET.CODE`

| Market | Prefix | Example | Company |
|--------|--------|---------|---------|
| Hong Kong | HK | HK.00700 | Tencent |
| US | US | US.AAPL | Apple |
| Shanghai | SH | SH.600519 | Moutai |
| Shenzhen | SZ | SZ.000001 | Ping An Bank |

## Command Options

- `--max N`: Get up to N news items per stock (default: 20)
- `--delay N`: Request delay in seconds (default: 1.0)
- `--json`: Output in JSON format

## Examples

```
# Single stock
/sina-finance-news HK.00700

# Multiple stocks
/sina-finance-news HK.00700 US.AAPL SH.600519

# Limit results
/sina-finance-news US.NVDA --max 5

# JSON output
/sina-finance-news HK.00700 --json
```

## Output Format

Each news item includes:
- **Title**: News headline
- **Time**: Publication time (YYYY-MM-DD HH:MM)
- **URL**: Link to full article

## Configuration (Optional)

See [OPENCLAW_CONFIG.md](OPENCLAW_CONFIG.md) for advanced configuration options.

## Standalone Usage

You can also use this as a standalone Python tool without OpenClaw. See the original [QUICKSTART.md](QUICKSTART.md) or [README.md](README.md) for details.

## Troubleshooting

**Skill not showing up?**
- Make sure the folder is in `~/.openclaw/skills/sina-finance-news`
- Check that `SKILL.md` exists in the folder
- Restart OpenClaw

**Dependencies not installed?**
- OpenClaw should auto-install `scrapling`
- Or manually: `pip install scrapling[all]>=0.4.0`

**Getting no results?**
- Check stock code format (MARKET.CODE)
- Verify network connectivity to sina.com.cn
- Try increasing `--delay` to avoid rate limiting
