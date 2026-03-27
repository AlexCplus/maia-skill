import json

# Input JSON from the prompt
input_data = {
  "brand": "Tododeia",
  "creator": "@soyenriquerocha",
  "generated_at": "2026-03-25T15:00:00Z",
  "risk_profile": "aggressive",
  "executive_summary": "On March 25, 2026, the market presents a high-octane environment defined by the 'AI Infrastructure' build-out and a resurgent US Dollar. We are witnessing a decoupling where Bitcoin rallies alongside the Dollar, suggesting a broad flight to quality assets. The strategy favors aggressive positioning in AI-industrial hybrids (Vertiv, Coherent), high-conviction crypto catalysts (Bitcoin options, Solana volume), and structural commodity deficits (Copper). Short-term volatility in Forex offers speculative upside in USD/MXN.",
  "macro_environment": {
    "trend": "Bullish Volatility",
    "key_drivers": [
      "AI Infrastructure Spending (Data Centers/Power)",
      "US Dollar Strength (DXY > 100)",
      "Crypto Institutional Flows",
      "Electrification Supply Deficits"
    ],
    "inflation_outlook": "Persistent pressures in commodities (Food/Gold)",
    "global_sentiment": "Risk-On for Tech/Crypto, Risk-Off for EM Currencies"
  },
  "portfolio_allocation": {
    "crypto": 40,
    "stocks": 35,
    "materials": 15,
    "currencies": 10,
    "rationale": "Overweight Crypto and Tech Stocks to capture high-beta upside from current catalysts. Materials provide essential structural exposure to the tech boom. Currencies serve as a tactical hedge and volatility play."
  },
  "cross_sector_insights": [
    "**The AI-Materials Nexus**: The surge in AI hardware stocks (Vertiv, Coherent) is directly fueling the 'supercycle' thesis for Copper and Lithium. Long both sectors for compounded exposure.",
    "**The Safe-Haven Divergence**: Bitcoin and Gold are rallying simultaneously with the US Dollar, breaking traditional inverse correlations. This indicates a unique 'everything hard' rally against fiat instability outside the USD.",
    "**Tech vs. Rates**: Despite the strong Dollar (usually bad for tech), the NASDAQ ignores the DXY due to overwhelming earnings growth from AI implementation."
  ],
  "risk_adjusted_picks": [
    {
      "asset": "Bitcoin (BTC)",
      "sector": "crypto",
      "action": "buy",
      "weight": "High",
      "reasoning": "Immediate $75k target driven by options expiry and institutional inflows. Breakout imminent."
    },
    {
      "asset": "Vertiv Holdings (VRT)",
      "sector": "stocks",
      "action": "strong_buy",
      "weight": "High",
      "reasoning": "The 'Index Inclusion Effect' combined with AI power demands makes this the premier industrial-tech play of Q1 2026."
    },
    {
      "asset": "Copper (HG)",
      "sector": "materials",
      "action": "buy",
      "weight": "Medium",
      "reasoning": "Critical infrastructure play. You cannot build the data centers for VRT/LITE without the copper."
    },
    {
      "asset": "USD/MXN",
      "sector": "currencies",
      "action": "buy",
      "weight": "Low",
      "reasoning": "Tactical trade on volatility. As DXY breaks 100, emerging market carry trades are unwinding rapidly."
    },
    {
      "asset": "Solana (SOL)",
      "sector": "crypto",
      "action": "buy",
      "weight": "Medium",
      "reasoning": "High-beta crypto play. Outperforming ETH on volume and user activity metrics."
    }
  ],
  "historical_accuracy": None,
  "warnings": [
    "**DXY Resistance**: If the Dollar Index fails at 102, expect a sharp reversal in USD/MXN.",
    "**Regulatory Risk**: Keep tight stops on Crypto assets; while news is good, volatility remains extreme.",
    "**Overheating**: AI stocks are at high valuations; monitor for any earnings misses in the semiconductor sector."
  ],
  "sectors": {
    "crypto": {
      "sector": "crypto",
      "timestamp": "2026-03-25T14:30:00Z",
      "assets": [
        {
          "name": "Bitcoin",
          "symbol": "BTC",
          "current_price": "$71,336.00",
          "change_24h": "+0.84%",
          "change_7d": "+0.09%",
          "change_30d": "+12.5%",
          "ytd_change": "+45.2%",
          "week_52_high": "$73,800.00",
          "week_52_low": "$38,500.00",
          "market_cap": "$1.43T",
          "volume_24h": "$36.36B",
          "sentiment": "bullish",
          "social_sentiment": "bullish",
          "social_buzz": "high",
          "confidence": 8,
          "source_agreement": "high",
          "sources_checked": [
            "coinmarketcap.com",
            "coingecko.com"
          ],
          "key_news": [
            "14B options expiry could push BTC to 75K",
            "CFTC launches innovation task force for crypto"
          ],
          "social_highlights": [
            "Traders eyeing $75k breakout on options expiry",
            "Institutional inflows remaining strong"
          ],
          "recommendation": "buy",
          "reasoning": "Bitcoin is showing strength near all-time highs with a major options expiry catalyst potentially driving price to $75k. Institutional support remains robust."
        },
        {
          "name": "Ethereum",
          "symbol": "ETH",
          "current_price": "$2,172.42",
          "change_24h": "+0.64%",
          "change_7d": "+1.15%",
          "change_30d": "-2.4%",
          "ytd_change": "+15.8%",
          "week_52_high": "$2,800.00",
          "week_52_low": "$1,550.00",
          "market_cap": "$262.16B",
          "volume_24h": "$17.21B",
          "sentiment": "neutral",
          "social_sentiment": "mixed",
          "social_buzz": "medium",
          "confidence": 6,
          "source_agreement": "high",
          "sources_checked": [
            "coinmarketcap.com",
            "coingecko.com"
          ],
          "key_news": [
            "Ethereum foundation selling pressure concerns",
            "Layer 2 adoption metrics hit record highs"
          ],
          "social_highlights": [
            "Debate over ETH underperformance vs BTC",
            "DeFi TVL growing on L2s"
          ],
          "recommendation": "hold",
          "reasoning": "Ethereum is lagging behind Bitcoin's momentum. While fundamentals (L2 growth) are strong, price action is currently consolidating. Wait for a breakout above $2,300."
        },
        {
          "name": "XRP",
          "symbol": "XRP",
          "current_price": "$1.41",
          "change_24h": "+0.25%",
          "change_7d": "+3.00%",
          "change_30d": "+18.2%",
          "ytd_change": "+85.5%",
          "week_52_high": "$1.50",
          "week_52_low": "$0.48",
          "market_cap": "$86.86B",
          "volume_24h": "$1.94B",
          "sentiment": "bullish",
          "social_sentiment": "bullish",
          "social_buzz": "high",
          "confidence": 7,
          "source_agreement": "medium",
          "sources_checked": [
            "coinmarketcap.com",
            "coindesk.com"
          ],
          "key_news": [
            "Ripple legal clarity driving institutional interest",
            "New cross-border payment partnerships announced"
          ],
          "social_highlights": [
            "XRP army targeting $2.00 next",
            "Speculation on ETF filing"
          ],
          "recommendation": "buy",
          "reasoning": "XRP is showing strong relative strength with a +3% weekly gain, outperforming the broader market. Technical setup points to a continuation toward $1.50."
        },
        {
          "name": "Solana",
          "symbol": "SOL",
          "current_price": "$91.60",
          "change_24h": "+1.04%",
          "change_7d": "+2.03%",
          "change_30d": "+8.5%",
          "ytd_change": "+110.2%",
          "week_52_high": "$126.00",
          "week_52_low": "$18.00",
          "market_cap": "$52.42B",
          "volume_24h": "$3.80B",
          "sentiment": "bullish",
          "social_sentiment": "bullish",
          "social_buzz": "high",
          "confidence": 7,
          "source_agreement": "high",
          "sources_checked": [
            "coinmarketcap.com",
            "coingecko.com"
          ],
          "key_news": [
            "Solana mobile phone sellout",
            "Network uptime stability improved"
          ],
          "social_highlights": [
            "Memecoin volume on Solana flipping Ethereum",
            "Developers flocking to ecosystem"
          ],
          "recommendation": "buy",
          "reasoning": "Solana continues to capture market share with high volume and user activity. Price is recovering well and showing bullish momentum."
        },
        {
          "name": "TRON",
          "symbol": "TRX",
          "current_price": "$0.3159",
          "change_24h": "+2.98%",
          "change_7d": "+3.80%",
          "change_30d": "+15.4%",
          "ytd_change": "+42.1%",
          "week_52_high": "$0.35",
          "week_52_low": "$0.10",
          "market_cap": "$29.94B",
          "volume_24h": "$501.77M",
          "sentiment": "bullish",
          "social_sentiment": "mixed",
          "social_buzz": "medium",
          "confidence": 6,
          "source_agreement": "high",
          "sources_checked": [
            "coinmarketcap.com",
            "coingecko.com"
          ],
          "key_news": [
            "USDT on Tron hits new milestone",
            "Deflationary burn mechanism accelerating"
          ],
          "social_highlights": [
            "Justin Sun announces new protocol upgrade",
            "Stablecoin usage dominance discussion"
          ],
          "recommendation": "buy",
          "reasoning": "TRX is the top gainer among major alts today (+2.98%). Its utility as the primary chain for USDT transfers provides a fundamental floor."
        }
      ],
      "sector_summary": "The crypto market is showing renewed strength led by Bitcoin pushing towards $75k ahead of a major options expiry. Altcoins like XRP and TRX are outperforming, while Ethereum lags slightly. Institutional interest remains the primary driver.",
      "sector_outlook": "bullish",
      "top_pick": "BTC",
      "top_pick_reasoning": "Bitcoin has the clearest catalyst (options expiry) and strongest institutional flows. Breaking $71k resistance opens the path to $75k in the short term."
    },
    "stocks": {
      "sector": "stocks",
      "timestamp": "2026-03-25T09:30:00Z",
      "assets": [
        {
          "name": "S&P 500",
          "symbol": "SPX",
          "current_price": "$6,248.50",
          "sentiment": "bullish",
          "confidence": 8,
          "recommendation": "buy",
          "reasoning": "The broader index continues to show strength, driven by persistent AI infrastructure spending and resilient consumer data. New additions in March 2026 reflect a rotation toward industrial tech and specialized hardware."
        },
        {
          "name": "NASDAQ Composite",
          "symbol": "IXIC",
          "current_price": "$21,415.20",
          "sentiment": "bullish",
          "confidence": 8,
          "recommendation": "buy",
          "reasoning": "Tech remains the primary driver of market returns. Despite high valuations, earnings growth from semiconductor and software sectors justifies current levels."
        },
        {
          "name": "Vertiv Holdings Co",
          "symbol": "VRT",
          "current_price": "$142.15",
          "sentiment": "very bullish",
          "confidence": 9,
          "recommendation": "strong buy",
          "reasoning": "Recently added to the S&P 500 on March 23, 2026. Dominant player in data center cooling and power management, crucial for the ongoing AI infrastructure build-out. Inclusion in the index will drive significant ETF buying pressure."
        },
        {
          "name": "Lumentum Holdings",
          "symbol": "LITE",
          "current_price": "$88.40",
          "sentiment": "bullish",
          "confidence": 7,
          "recommendation": "buy",
          "reasoning": "Another fresh S&P 500 addition (March 2026). As optical networking becomes critical for next-gen AI clusters, Lumentum's photonics portfolio is seeing accelerating demand. Analyst upgrades followed the index announcement."
        },
        {
          "name": "AppLovin Corp",
          "symbol": "APP",
          "current_price": "$115.75",
          "sentiment": "bullish",
          "confidence": 8,
          "recommendation": "buy",
          "reasoning": "Added to the S&P 500 in late 2025, AppLovin has cemented its leadership in mobile ad-tech. The company's AI-driven software platform continues to outperform legacy competitors, delivering consistent earnings beats."
        },
        {
          "name": "Coherent Corp",
          "symbol": "COHR",
          "current_price": "$92.30",
          "sentiment": "bullish",
          "confidence": 7,
          "recommendation": "buy",
          "reasoning": "New S&P 500 component (March 2026). A key supplier of engineered materials and lasers for semiconductor manufacturing and industrial applications. Benefiting from the reshoring of chip production and advanced manufacturing trends."
        },
        {
          "name": "Robinhood Markets",
          "symbol": "HOOD",
          "current_price": "$38.50",
          "sentiment": "neutral-bullish",
          "confidence": 6,
          "recommendation": "hold",
          "reasoning": "Since its S&P 500 inclusion in late 2025, HOOD has matured into a comprehensive financial services platform. While user growth remains strong, regulatory scrutiny creates some near-term headwinds, making it a solid hold with upside potential."
        }
      ],
      "sector_summary": "The market in March 2026 is defined by the 'Infrastructure Phase' of the AI revolution. Investors are rewarding companies that provide the physical and digital backbone for advanced computing—power, cooling, optics, and specialized hardware. The S&P 500's recent rebalancing explicitly favors these industrial-tech hybrids over legacy sectors.",
      "sector_outlook": "Positive. We anticipate the 'Index Inclusion Effect' to buoy the newly added names (VRT, LITE, COHR) through Q2 2026. Volatility may increase as inflation data is released later this month, but the structural trend remains upward for companies with clear AI-revenue attribution.",
      "top_pick": "Vertiv Holdings Co (VRT)"
    },
    "currencies": {
      "sector": "currencies",
      "timestamp": "2026-03-25T14:30:00Z",
      "assets": [
        {
          "name": "US Dollar Index",
          "symbol": "DXY",
          "current_price": "100.45",
          "sentiment": "bullish",
          "confidence": 9,
          "recommendation": "buy",
          "reasoning": "Breaking news indicates the Dollar has successfully reclaimed the psychological 100 level. Technical breakout confirms renewed strength amidst global flight to safety."
        },
        {
          "name": "US Dollar / Mexican Peso",
          "symbol": "USD/MXN",
          "current_price": "19.85",
          "sentiment": "bullish",
          "confidence": 8,
          "recommendation": "buy",
          "reasoning": "High volatility forecast for March 2026 confirmed. EM currencies are under pressure as DXY rises; peso weakening as carry trade unwinds."
        },
        {
          "name": "US Dollar / Japanese Yen",
          "symbol": "USD/JPY",
          "current_price": "148.20",
          "sentiment": "bullish",
          "confidence": 7,
          "recommendation": "buy",
          "reasoning": "Yield spread divergence continues to favor the Greenback. Key resistance at 150 is the next target as BoJ remains dovish."
        },
        {
          "name": "British Pound / US Dollar",
          "symbol": "GBP/USD",
          "current_price": "1.2150",
          "sentiment": "bearish",
          "confidence": 6,
          "recommendation": "sell",
          "reasoning": "Cable looks vulnerable as UK economic data softens against the resurgent US Dollar backdrop."
        },
        {
          "name": "Australian Dollar / US Dollar",
          "symbol": "AUD/USD",
          "current_price": "0.6380",
          "sentiment": "bearish",
          "confidence": 7,
          "recommendation": "sell",
          "reasoning": "Commodity currency weakness persists. Global growth concerns are weighing heavily on the Aussie dollar."
        },
        {
          "name": "US Dollar / South African Rand",
          "symbol": "USD/ZAR",
          "current_price": "19.10",
          "sentiment": "bullish",
          "confidence": 8,
          "recommendation": "buy",
          "reasoning": "Selected as a high-volatility play. ZAR is extremely sensitive to the stronger DXY environment, breaking technical resistance levels."
        }
      ],
      "sector_summary": "The currency market in March 2026 is defined by the resurgence of the US Dollar, with the DXY index reclaiming the critical 100 level. This move is triggering a broad sell-off in risk currencies (AUD, GBP) and putting severe pressure on Emerging Market pairs (MXN, ZAR). Volatility is elevated across the board as traders reposition for a prolonged period of USD strength.",
      "sector_outlook": "Expect continued USD dominance in the short term. The 'Reclaim 100' narrative is driving momentum. Look for opportunities to short high-beta currencies against the dollar. The trend is your friend until DXY faces resistance at 102.",
      "top_pick": "USD/MXN"
    },
    "materials": {
      "sector": "materials",
      "timestamp": "2026-03-25T08:30:00Z",
      "assets": [
        {
          "name": "Gold",
          "symbol": "XAU",
          "current_price": "2645.50",
          "sentiment": "bullish",
          "confidence": 8,
          "recommendation": "buy",
          "reasoning": "Persistent inflationary pressures and geopolitical uncertainty drive demand for safe-haven assets. Central bank accumulation continues to support price floors above $2500."
        },
        {
          "name": "Crude Oil WTI",
          "symbol": "CL",
          "current_price": "78.42",
          "sentiment": "neutral",
          "confidence": 6,
          "recommendation": "hold",
          "reasoning": "Balanced market with OPEC+ supply discipline countering weaker demand growth from accelerated EV adoption. Geopolitical risk premium remains a key swing factor."
        },
        {
          "name": "Copper",
          "symbol": "HG",
          "current_price": "4.85",
          "sentiment": "bullish",
          "confidence": 9,
          "recommendation": "strong_buy",
          "reasoning": "Critical supply deficit emerging as electrification infrastructure projects accelerate globally. 'The new oil' narrative is firmly established with dwindling inventories."
        },
        {
          "name": "Lithium Carbonate",
          "symbol": "LIT",
          "current_price": "28500.00",
          "sentiment": "bullish",
          "confidence": 7,
          "recommendation": "buy",
          "reasoning": "Stabilizing after volatility; demand from next-gen battery manufacturing facilities coming online in Q2 2026 is expected to outpace current extraction rates."
        },
        {
          "name": "Wheat",
          "symbol": "ZW",
          "current_price": "720.25",
          "sentiment": "bullish",
          "confidence": 7,
          "recommendation": "buy",
          "reasoning": "Climate anomalies in key growing regions (Australia/Russia) threaten yield forecasts for the 2026 harvest, driving food security concerns and speculative buying."
        }
      ],
      "sector_summary": "The materials sector in March 2026 is characterized by a divergence between traditional energy (Oil) and electrification metals (Copper, Lithium). Industrial metals are outperforming energy due to structural deficits driven by the green transition. Agricultural commodities face upward pressure from climate-related supply shocks.",
      "sector_outlook": "Positive. We anticipate the 'commodity supercycle' extension for critical minerals, while precious metals remain a robust hedge against fiat currency volatility. Energy markets will likely remain range-bound absent major supply disruptions.",
      "top_pick": "Copper"
    }
  }
}

# Translations
translations = {
    # Executive Summary
    input_data["executive_summary"]: "El 25 de marzo de 2026, el mercado presenta un entorno de alto octanaje definido por la expansión de la 'Infraestructura de IA' y un Dólar estadounidense resurgente. Estamos presenciando un desacoplamiento donde Bitcoin sube junto con el Dólar, sugiriendo una amplia huida hacia activos de calidad. La estrategia favorece un posicionamiento agresivo en híbridos industriales de IA (Vertiv, Coherent), catalizadores cripto de alta convicción (opciones de Bitcoin, volumen de Solana) y déficits estructurales de materias primas (Cobre). La volatilidad a corto plazo en Forex ofrece un potencial especulativo al alza en el USD/MXN.",
    
    # Macro Environment
    "Bullish Volatility": "Volatilidad Alcista",
    "Persistent pressures in commodities (Food/Gold)": "Presiones persistentes en materias primas (Alimentos/Oro)",
    "Risk-On for Tech/Crypto, Risk-Off for EM Currencies": "Apetito de riesgo para Tech/Cripto, Aversión al riesgo para divisas de Mercados Emergentes",
    "AI Infrastructure Spending (Data Centers/Power)": "Gasto en Infraestructura de IA (Centros de Datos/Energía)",
    "US Dollar Strength (DXY > 100)": "Fortaleza del Dólar estadounidense (DXY > 100)",
    "Crypto Institutional Flows": "Flujos Institucionales en Cripto",
    "Electrification Supply Deficits": "Déficits de Suministro para Electrificación",

    # Cross Sector Insights
    "**The AI-Materials Nexus**: The surge in AI hardware stocks (Vertiv, Coherent) is directly fueling the 'supercycle' thesis for Copper and Lithium. Long both sectors for compounded exposure.": "**El Nexo IA-Materiales**: El auge en las acciones de hardware de IA (Vertiv, Coherent) está alimentando directamente la tesis del 'superciclo' para el Cobre y el Litio. Largo en ambos sectores para una exposición compuesta.",
    "**The Safe-Haven Divergence**: Bitcoin and Gold are rallying simultaneously with the US Dollar, breaking traditional inverse correlations. This indicates a unique 'everything hard' rally against fiat instability outside the USD.": "**La Divergencia de Refugio Seguro**: Bitcoin y el Oro están subiendo simultáneamente con el Dólar estadounidense, rompiendo las correlaciones inversas tradicionales. Esto indica un repunte único de 'todo lo duro' contra la inestabilidad fiduciaria fuera del USD.",
    "**Tech vs. Rates**: Despite the strong Dollar (usually bad for tech), the NASDAQ ignores the DXY due to overwhelming earnings growth from AI implementation.": "**Tecnología vs. Tasas**: A pesar del Dólar fuerte (generalmente malo para la tecnología), el NASDAQ ignora el DXY debido al abrumador crecimiento de las ganancias por la implementación de la IA.",

    # Warnings
    "**DXY Resistance**: If the Dollar Index fails at 102, expect a sharp reversal in USD/MXN.": "**Resistencia del DXY**: Si el Índice del Dólar falla en 102, espere una reversión brusca en el USD/MXN.",
    "**Regulatory Risk**: Keep tight stops on Crypto assets; while news is good, volatility remains extreme.": "**Riesgo Regulatorio**: Mantenga stops ajustados en activos Cripto; aunque las noticias son buenas, la volatilidad sigue siendo extrema.",
    "**Overheating**: AI stocks are at high valuations; monitor for any earnings misses in the semiconductor sector.": "**Sobrecalentamiento**: Las acciones de IA están en valoraciones altas; monitoree cualquier fallo en las ganancias en el sector de semiconductores.",

    # Risk Adjusted Picks Reasoning
    "Immediate $75k target driven by options expiry and institutional inflows. Breakout imminent.": "Objetivo inmediato de $75k impulsado por el vencimiento de opciones y flujos institucionales. Ruptura inminente.",
    "The 'Index Inclusion Effect' combined with AI power demands makes this the premier industrial-tech play of Q1 2026.": "El 'Efecto de Inclusión en el Índice' combinado con las demandas de energía de la IA lo convierte en la principal jugada industrial-tecnológica del T1 2026.",
    "Critical infrastructure play. You cannot build the data centers for VRT/LITE without the copper.": "Jugada de infraestructura crítica. No se pueden construir los centros de datos para VRT/LITE sin el cobre.",
    "Tactical trade on volatility. As DXY breaks 100, emerging market carry trades are unwinding rapidly.": "Comercio táctico sobre volatilidad. A medida que el DXY rompe los 100, las operaciones de carry trade en mercados emergentes se están deshaciendo rápidamente.",
    "High-beta crypto play. Outperforming ETH on volume and user activity metrics.": "Jugada cripto de beta alta. Superando a ETH en métricas de volumen y actividad de usuarios.",

    # Sectors: Crypto
    "The crypto market is showing renewed strength led by Bitcoin pushing towards $75k ahead of a major options expiry. Altcoins like XRP and TRX are outperforming, while Ethereum lags slightly. Institutional interest remains the primary driver.": "El mercado cripto muestra una fuerza renovada liderada por Bitcoin empujando hacia los $75k antes de un importante vencimiento de opciones. Las altcoins como XRP y TRX están superando el rendimiento, mientras que Ethereum se queda un poco atrás. El interés institucional sigue siendo el principal motor.",
    "Bitcoin has the clearest catalyst (options expiry) and strongest institutional flows. Breaking $71k resistance opens the path to $75k in the short term.": "Bitcoin tiene el catalizador más claro (vencimiento de opciones) y los flujos institucionales más fuertes. Romper la resistencia de $71k abre el camino a $75k en el corto plazo.",
    
    # Crypto Assets
    "14B options expiry could push BTC to 75K": "Vencimiento de opciones de 14MM podría empujar a BTC a 75K",
    "CFTC launches innovation task force for crypto": "La CFTC lanza un grupo de trabajo de innovación para cripto",
    "Traders eyeing $75k breakout on options expiry": "Los traders observan la ruptura de $75k en el vencimiento de opciones",
    "Institutional inflows remaining strong": "Los flujos institucionales se mantienen fuertes",
    "Bitcoin is showing strength near all-time highs with a major options expiry catalyst potentially driving price to $75k. Institutional support remains robust.": "Bitcoin muestra fortaleza cerca de máximos históricos con un catalizador importante de vencimiento de opciones que potencialmente impulsará el precio a $75k. El apoyo institucional sigue siendo robusto.",
    
    "Ethereum foundation selling pressure concerns": "Preocupaciones por la presión de venta de la fundación Ethereum",
    "Layer 2 adoption metrics hit record highs": "Las métricas de adopción de Capa 2 alcanzan máximos históricos",
    "Debate over ETH underperformance vs BTC": "Debate sobre el bajo rendimiento de ETH frente a BTC",
    "DeFi TVL growing on L2s": "El TVL de DeFi creciendo en L2s",
    "Ethereum is lagging behind Bitcoin's momentum. While fundamentals (L2 growth) are strong, price action is currently consolidating. Wait for a breakout above $2,300.": "Ethereum se está quedando atrás del impulso de Bitcoin. Aunque los fundamentos (crecimiento de L2) son fuertes, la acción del precio se está consolidando actualmente. Espere una ruptura por encima de $2,300.",
    
    "Ripple legal clarity driving institutional interest": "La claridad legal de Ripple impulsa el interés institucional",
    "New cross-border payment partnerships announced": "Anunciadas nuevas asociaciones de pagos transfronterizos",
    "XRP army targeting $2.00 next": "El ejército de XRP apunta a $2.00 a continuación",
    "Speculation on ETF filing": "Especulación sobre la solicitud de ETF",
    "XRP is showing strong relative strength with a +3% weekly gain, outperforming the broader market. Technical setup points to a continuation toward $1.50.": "XRP muestra una fuerte fuerza relativa con una ganancia semanal del +3%, superando al mercado en general. La configuración técnica apunta a una continuación hacia $1.50.",

    "Solana mobile phone sellout": "Agotamiento del teléfono móvil Solana",
    "Network uptime stability improved": "Mejorada la estabilidad del tiempo de actividad de la red",
    "Memecoin volume on Solana flipping Ethereum": "El volumen de Memecoins en Solana superando a Ethereum",
    "Developers flocking to ecosystem": "Desarrolladores acudiendo en masa al ecosistema",
    "Solana continues to capture market share with high volume and user activity. Price is recovering well and showing bullish momentum.": "Solana continúa capturando cuota de mercado con alto volumen y actividad de usuarios. El precio se está recuperando bien y mostrando un impulso alcista.",
    
    "USDT on Tron hits new milestone": "USDT en Tron alcanza un nuevo hito",
    "Deflationary burn mechanism accelerating": "Mecanismo de quema deflacionaria acelerándose",
    "Justin Sun announces new protocol upgrade": "Justin Sun anuncia nueva actualización del protocolo",
    "Stablecoin usage dominance discussion": "Discusión sobre el dominio del uso de stablecoins",
    "TRX is the top gainer among major alts today (+2.98%). Its utility as the primary chain for USDT transfers provides a fundamental floor.": "TRX es el mayor ganador entre las principales alts hoy (+2.98%). Su utilidad como la cadena principal para transferencias de USDT proporciona un piso fundamental.",
    
    # Sectors: Stocks
    "The market in March 2026 is defined by the 'Infrastructure Phase' of the AI revolution. Investors are rewarding companies that provide the physical and digital backbone for advanced computing—power, cooling, optics, and specialized hardware. The S&P 500's recent rebalancing explicitly favors these industrial-tech hybrids over legacy sectors.": "El mercado en marzo de 2026 se define por la 'Fase de Infraestructura' de la revolución de la IA. Los inversores están recompensando a las empresas que proporcionan la columna vertebral física y digital para la computación avanzada: energía, refrigeración, óptica y hardware especializado. El reciente reequilibrio del S&P 500 favorece explícitamente a estos híbridos industriales-tecnológicos sobre los sectores tradicionales.",
    
    # Stock Assets
    "The broader index continues to show strength, driven by persistent AI infrastructure spending and resilient consumer data. New additions in March 2026 reflect a rotation toward industrial tech and specialized hardware.": "El índice general continúa mostrando fortaleza, impulsado por el gasto persistente en infraestructura de IA y datos de consumo resilientes. Las nuevas incorporaciones en marzo de 2026 reflejan una rotación hacia la tecnología industrial y el hardware especializado.",
    "Tech remains the primary driver of market returns. Despite high valuations, earnings growth from semiconductor and software sectors justifies current levels.": "La tecnología sigue siendo el principal motor de los rendimientos del mercado. A pesar de las altas valoraciones, el crecimiento de las ganancias de los sectores de semiconductores y software justifica los niveles actuales.",
    "Recently added to the S&P 500 on March 23, 2026. Dominant player in data center cooling and power management, crucial for the ongoing AI infrastructure build-out. Inclusion in the index will drive significant ETF buying pressure.": "Recientemente agregado al S&P 500 el 23 de marzo de 2026. Jugador dominante en refrigeración de centros de datos y gestión de energía, crucial para la expansión continua de la infraestructura de IA. La inclusión en el índice impulsará una presión de compra significativa de ETF.",
    "Another fresh S&P 500 addition (March 2026). As optical networking becomes critical for next-gen AI clusters, Lumentum's photonics portfolio is seeing accelerating demand. Analyst upgrades followed the index announcement.": "Otra nueva incorporación al S&P 500 (marzo de 2026). A medida que las redes ópticas se vuelven críticas para los clústeres de IA de próxima generación, la cartera de fotónica de Lumentum está viendo una demanda acelerada. Las actualizaciones de analistas siguieron al anuncio del índice.",
    "Added to the S&P 500 in late 2025, AppLovin has cemented its leadership in mobile ad-tech. The company's AI-driven software platform continues to outperform legacy competitors, delivering consistent earnings beats.": "Agregado al S&P 500 a fines de 2025, AppLovin ha consolidado su liderazgo en tecnología publicitaria móvil. La plataforma de software impulsada por IA de la compañía continúa superando a los competidores tradicionales, entregando ganancias consistentes.",
    "New S&P 500 component (March 2026). A key supplier of engineered materials and lasers for semiconductor manufacturing and industrial applications. Benefiting from the reshoring of chip production and advanced manufacturing trends.": "Nuevo componente del S&P 500 (marzo de 2026). Un proveedor clave de materiales de ingeniería y láseres para la fabricación de semiconductores y aplicaciones industriales. Beneficiándose de la relocalización de la producción de chips y las tendencias de fabricación avanzada.",
    "Since its S&P 500 inclusion in late 2025, HOOD has matured into a comprehensive financial services platform. While user growth remains strong, regulatory scrutiny creates some near-term headwinds, making it a solid hold with upside potential.": "Desde su inclusión en el S&P 500 a fines de 2025, HOOD ha madurado hasta convertirse en una plataforma integral de servicios financieros. Si bien el crecimiento de usuarios sigue siendo fuerte, el escrutinio regulatorio crea algunos vientos en contra a corto plazo, convirtiéndolo en una retención sólida con potencial alcista.",
    
    # Sectors: Currencies
    "The currency market in March 2026 is defined by the resurgence of the US Dollar, with the DXY index reclaiming the critical 100 level. This move is triggering a broad sell-off in risk currencies (AUD, GBP) and putting severe pressure on Emerging Market pairs (MXN, ZAR). Volatility is elevated across the board as traders reposition for a prolonged period of USD strength.": "El mercado de divisas en marzo de 2026 se define por el resurgimiento del Dólar estadounidense, con el índice DXY reclamando el nivel crítico de 100. Este movimiento está provocando una venta masiva en divisas de riesgo (AUD, GBP) y ejerciendo una fuerte presión sobre los pares de Mercados Emergentes (MXN, ZAR). La volatilidad es elevada en general a medida que los traders se reposicionan para un período prolongado de fortaleza del USD.",
    
    # Currency Assets
    "Breaking news indicates the Dollar has successfully reclaimed the psychological 100 level. Technical breakout confirms renewed strength amidst global flight to safety.": "Noticias de última hora indican que el Dólar ha recuperado con éxito el nivel psicológico de 100. La ruptura técnica confirma una fuerza renovada en medio de una huida global hacia la seguridad.",
    "High volatility forecast for March 2026 confirmed. EM currencies are under pressure as DXY rises; peso weakening as carry trade unwinds.": "Pronóstico de alta volatilidad para marzo de 2026 confirmado. Las divisas de ME están bajo presión a medida que sube el DXY; debilitamiento del peso a medida que se deshace el carry trade.",
    "Yield spread divergence continues to favor the Greenback. Key resistance at 150 is the next target as BoJ remains dovish.": "La divergencia del diferencial de rendimiento continúa favoreciendo al Billete Verde. La resistencia clave en 150 es el próximo objetivo ya que el BoJ sigue siendo moderado.",
    "Cable looks vulnerable as UK economic data softens against the resurgent US Dollar backdrop.": "El Cable parece vulnerable a medida que los datos económicos del Reino Unido se suavizan frente al resurgente telón de fondo del Dólar estadounidense.",
    "Commodity currency weakness persists. Global growth concerns are weighing heavily on the Aussie dollar.": "Persiste la debilidad de las divisas de materias primas. Las preocupaciones sobre el crecimiento global pesan mucho sobre el dólar australiano.",
    "Selected as a high-volatility play. ZAR is extremely sensitive to the stronger DXY environment, breaking technical resistance levels.": "Seleccionado como una jugada de alta volatilidad. El ZAR es extremadamente sensible al entorno de DXY más fuerte, rompiendo niveles de resistencia técnica.",
    
    # Sectors: Materials
    "The materials sector in March 2026 is characterized by a divergence between traditional energy (Oil) and electrification metals (Copper, Lithium). Industrial metals are outperforming energy due to structural deficits driven by the green transition. Agricultural commodities face upward pressure from climate-related supply shocks.": "El sector de materiales en marzo de 2026 se caracteriza por una divergencia entre la energía tradicional (Petróleo) y los metales de electrificación (Cobre, Litio). Los metales industriales están superando a la energía debido a déficits estructurales impulsados por la transición verde. Los productos agrícolas enfrentan presión al alza por choques de oferta relacionados con el clima.",
    
    # Material Assets
    "Persistent inflationary pressures and geopolitical uncertainty drive demand for safe-haven assets. Central bank accumulation continues to support price floors above $2500.": "Las presiones inflacionarias persistentes y la incertidumbre geopolítica impulsan la demanda de activos de refugio seguro. La acumulación de los bancos centrales continúa respaldando los pisos de precios por encima de $2500.",
    "Balanced market with OPEC+ supply discipline countering weaker demand growth from accelerated EV adoption. Geopolitical risk premium remains a key swing factor.": "Mercado equilibrado con disciplina de oferta de la OPEP+ contrarrestando el crecimiento más débil de la demanda por la adopción acelerada de vehículos eléctricos. La prima de riesgo geopolítico sigue siendo un factor oscilante clave.",
    "Critical supply deficit emerging as electrification infrastructure projects accelerate globally. 'The new oil' narrative is firmly established with dwindling inventories.": "Déficit de suministro crítico emergiendo a medida que los proyectos de infraestructura de electrificación se aceleran a nivel mundial. La narrativa del 'nuevo petróleo' está firmemente establecida con inventarios menguantes.",
    "Stabilizing after volatility; demand from next-gen battery manufacturing facilities coming online in Q2 2026 is expected to outpace current extraction rates.": "Estabilizándose después de la volatilidad; se espera que la demanda de las instalaciones de fabricación de baterías de próxima generación que entrarán en funcionamiento en el T2 2026 supere las tasas de extracción actuales.",
    "Climate anomalies in key growing regions (Australia/Russia) threaten yield forecasts for the 2026 harvest, driving food security concerns and speculative buying.": "Anomalías climáticas en regiones clave de cultivo (Australia/Rusia) amenazan los pronósticos de rendimiento para la cosecha de 2026, impulsando preocupaciones de seguridad alimentaria y compras especulativas."
}

def translate_value(value):
    if value in translations:
        return translations[value]
    return value

# Apply translations
input_data["executive_summary"] = translate_value(input_data["executive_summary"])

input_data["macro_environment"]["trend"] = translate_value(input_data["macro_environment"]["trend"])
input_data["macro_environment"]["inflation_outlook"] = translate_value(input_data["macro_environment"]["inflation_outlook"])
input_data["macro_environment"]["global_sentiment"] = translate_value(input_data["macro_environment"]["global_sentiment"])
input_data["macro_environment"]["key_drivers"] = [translate_value(x) for x in input_data["macro_environment"]["key_drivers"]]

input_data["cross_sector_insights"] = [translate_value(x) for x in input_data["cross_sector_insights"]]
input_data["warnings"] = [translate_value(x) for x in input_data["warnings"]]

for pick in input_data["risk_adjusted_picks"]:
    pick["reasoning"] = translate_value(pick["reasoning"])

for sector_name, sector_data in input_data["sectors"].items():
    if "sector_summary" in sector_data:
        sector_data["sector_summary"] = translate_value(sector_data["sector_summary"])
    if "top_pick_reasoning" in sector_data:
        sector_data["top_pick_reasoning"] = translate_value(sector_data["top_pick_reasoning"])
    
    if "assets" in sector_data:
        for asset in sector_data["assets"]:
            if "reasoning" in asset:
                asset["reasoning"] = translate_value(asset["reasoning"])
            if "key_news" in asset:
                asset["key_news"] = [translate_value(x) for x in asset["key_news"]]
            if "social_highlights" in asset:
                asset["social_highlights"] = [translate_value(x) for x in asset["social_highlights"]]

# Print final JSON
print(json.dumps(input_data, indent=2, ensure_ascii=False))
