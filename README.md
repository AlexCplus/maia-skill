# Tododeia — Multi-Agent Investment Analysis v2

**by @soyenriquerocha**

A Claude Code skill that spawns 5 specialized AI research agents to analyze investment opportunities across crypto, stocks, forex, and commodities. Adapts to your risk profile, tracks historical accuracy, analyzes social sentiment, and generates an interactive branded HTML report.

## How It Works

```
                         ┌──────────────┐
                    ┌────┤  You trigger  ├────┐
                    │    │  "analyze     │    │
                    │    │   markets"    │    │
                    │    └──────────────┘    │
                    ▼                        ▼
            ┌──────────────┐        ┌──────────────┐
            │ Risk Profile │        │ Load History  │
            │   Question   │        │  (if exists)  │
            └──────┬───────┘        └──────┬───────┘
                   │                       │
                   ▼                       │
    ┌──────────────────────────────┐       │
    │     4 Sector Agents          │       │
    │  (parallel web research)     │       │
    │                              │       │
    │  ┌───────┐  ┌───────┐       │       │
    │  │Crypto │  │Stocks │       │       │
    │  └───────┘  └───────┘       │       │
    │  ┌───────┐  ┌──────────┐   │       │
    │  │ Forex │  │Materials │   │       │
    │  └───────┘  └──────────┘   │       │
    └──────────────┬───────────────┘       │
                   │                       │
                   ▼                       ▼
          ┌────────────────────────────────────┐
          │        Strategy Agent               │
          │  (cross-sector analysis,            │
          │   risk-adjusted ranking,            │
          │   portfolio allocation,             │
          │   historical accuracy check)        │
          └────────────────┬───────────────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │  Interactive     │
                  │  HTML Report     │
                  │  localhost:8420  │
                  └──────────────────┘
```

## Features

- **5 AI Agents**: 4 sector researchers + 1 strategy synthesizer
- **Risk Profiles**: Conservative, moderate, or aggressive — recommendations adapt to you
- **Social Sentiment**: Twitter/X and Reddit sentiment analysis per asset
- **Source Verification**: Cross-references prices from 2+ sources with agreement scoring
- **Historical Context**: YTD performance, 52-week ranges, not just today's snapshot
- **Accuracy Tracking**: Compares past recommendations to actual outcomes
- **Portfolio Allocation**: Suggested % allocation across sectors based on your risk profile
- **Cross-Sector Insights**: Correlations and divergences that individual agents can't see
- **Interactive Report**: Sortable tables, filter by signal (buy/hold/sell), search assets, print-friendly
- **Scheduling**: Option to run daily or weekly with automatic reports

## Sectors Covered

| Sector | Assets |
|--------|--------|
| Crypto | BTC, ETH, SOL, XRP, BNB |
| Stocks | S&P 500, NASDAQ, AAPL, NVDA, MSFT, GOOGL, TSLA |
| Forex | EUR/USD, GBP/USD, USD/JPY, USD/MXN, DXY |
| Commodities | Gold, Silver, Oil (WTI), Natural Gas, Copper |

## Installation

```bash
git clone https://github.com/Hainrixz/jere-noticias-inver.git ~/.claude/skills/jere-noticias-inver
```

That's it. The skill auto-activates when you mention investment-related topics.

## Usage

In any Claude Code conversation:

- "Run an investment analysis"
- "What are the best investment opportunities today?"
- "Analyze the markets"
- "Give me a market report"

You'll be asked your risk profile, then the agents go to work. Report opens at `http://localhost:8420/report.html`.

### Scheduling (Optional)

After your first report, you can set up recurring analysis:

```
/loop 24h /investment-analysis    # Daily reports
/loop 168h /investment-analysis   # Weekly reports
```

## Customization

### Branding

Edit CSS variables in `assets/template.html`:

```css
:root {
  --brand-accent: #e94560;
  --brand-primary: #0a0e1a;
  --sector-crypto: #f7931a;
  --sector-stocks: #00c853;
  --sector-currencies: #2196f3;
  --sector-materials: #ffc107;
}
```

### Assets

Edit `references/agent-prompts.md` to change which assets each agent researches.

### Risk Profiles

The Strategy Agent prompt in `references/agent-prompts.md` defines how each risk profile affects scoring and allocation. Customize the multipliers and allocation ranges there.

## Report Features

The interactive HTML report includes:

- **Executive summary** with macro environment assessment
- **Portfolio allocation** bar chart and doughnut chart
- **Risk-adjusted top picks** with confidence meters and position sizing
- **Cross-sector insights** highlighting correlations
- **4 sector detail panels** with sortable asset tables
- **Social buzz chart** showing which sectors are trending
- **Risk vs. Confidence bubble chart** for visual comparison
- **Historical accuracy ring** tracking past performance
- **Risk warnings** when the strategy agent detects concerns
- **Filter toolbar** — show only buys, search by asset name
- **Print/PDF button** — clean print-optimized layout

## Disclaimer

This tool is for **informational and educational purposes only**. It does not constitute financial advice, investment recommendations, or solicitation to buy or sell any securities, cryptocurrencies, or commodities. AI-generated analysis may contain errors and should not be relied upon for investment decisions. Always consult a qualified financial advisor before making investment decisions. Past performance is not indicative of future results. Tododeia and its creators assume no liability for investment losses.

## License

MIT — see [LICENSE](LICENSE)

## Contributing

Open source. PRs welcome!
