# OpenClaw 配置示例

这是一个可选的配置文件示例，展示如何在 OpenClaw 中配置 sina-finance-news skill。

## openclaw.json 配置示例

```json5
{
  "skills": {
    "entries": {
      "sina-finance-news": {
        "enabled": true,
        "config": {
          // 默认每个股票获取的新闻数量
          "defaultMaxNews": 20,

          // 默认请求延迟（秒）
          "defaultDelay": 1.5,

          // 默认输出格式：text 或 json
          "defaultFormat": "text",

          // 关注的股票列表（可选）
          "watchlist": [
            "HK.00700",   // 腾讯
            "US.AAPL",    // 苹果
            "SH.600519",  // 茅台
            "SZ.000001"   // 平安银行
          ]
        }
      }
    }
  }
}
```

## 说明

### enabled
- 类型：`boolean`
- 默认：`true`
- 说明：是否启用此 skill

### config.defaultMaxNews
- 类型：`number`
- 默认：`20`
- 说明：每个股票默认获取的新闻数量，可以在调用时通过 `--max` 参数覆盖

### config.defaultDelay
- 类型：`number`
- 默认：`1.0`
- 说明：请求间隔时间（秒），用于反爬控制。生产环境建议设置为 2.0 或更高

### config.defaultFormat
- 类型：`string`
- 可选值：`text` 或 `json`
- 默认：`text`
- 说明：默认输出格式

### config.watchlist
- 类型：`array<string>`
- 说明：可选的关注股票列表，方便快速查询

## 使用配置

配置文件应该放在以下位置之一：
- `~/.openclaw/openclaw.json`
- 项目根目录下的 `openclaw.json`

如果不提供配置文件，skill 将使用默认值。

## 在 OpenClaw 中使用

配置好后，你可以这样使用：

```
# 使用默认配置获取新闻
/sina-finance-news HK.00700

# 覆盖默认配置
/sina-finance-news US.AAPL --max 50 --delay 2

# 批量查询关注列表（需要手动指定）
/sina-finance-news HK.00700 US.AAPL SH.600519 SZ.000001
```

或者直接对话：

```
帮我查一下腾讯最近的新闻
给我看看我关注的股票的最新消息
```
