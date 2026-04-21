from flask import Flask
import board
import adafruit_dht
import time
import requests

app = Flask(__name__)

# DHT11 on GPIO17
dht = adafruit_dht.DHT11(board.D17)

# ── Telegram config ───────────────────────────────────────
TELEGRAM_TOKEN   = "YOUR_BOT_TOKEN"       # from @BotFather
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"         # from getUpdates
# ─────────────────────────────────────────────────────────

# Prevent spamming — only alert once per risk level until it drops back down
last_alert_level = None


def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message})
        print(f"Telegram sent: {message}")
    except Exception as e:
        print(f"Telegram failed: {e}")


def maybe_alert(risk, temp, hum):
    global last_alert_level

    if risk >= 80 and last_alert_level != "critical":
        send_telegram(
            f"🚨 CRITICAL mildew risk!\n"
            f"Risk: {risk}/100\n"
            f"Temp: {temp}°C | Humidity: {hum}%\n"
            f"Act now — consider fungicide application."
        )
        last_alert_level = "critical"

    elif risk >= 50 and last_alert_level not in ("moderate", "critical"):
        send_telegram(
            f"⚠️ Moderate mildew risk detected.\n"
            f"Risk: {risk}/100\n"
            f"Temp: {temp}°C | Humidity: {hum}%\n"
            f"Monitor closely."
        )
        last_alert_level = "moderate"

    elif risk < 50:
        last_alert_level = None   # reset so next spike triggers a fresh alert


def risk_score(temp, hum):
    if temp is None or hum is None:
        return 0
    if temp < 14:
        return 20
    elif hum < 82:
        return 60
    else:
        return 90


def read_sensor():
    try:
        temp = dht.temperature
        hum = dht.humidity
        return temp, hum
    except RuntimeError:
        return None, None


@app.route("/")
def home():

    temp, hum = read_sensor()

    # retry once if failed
    if temp is None or hum is None:
        time.sleep(1)
        temp, hum = read_sensor()

    if temp is None or hum is None:
        return "<h1>Sensor reading failed</h1>"

    risk = risk_score(temp, hum)

    color = "green"
    if risk >= 80:
        color = "red"
    elif risk >= 50:
        color = "orange"

    # Send Telegram alert if needed
    maybe_alert(risk, temp, hum)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta http-equiv="refresh" content="3">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mildew Monitor — Live</title>
    <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Playfair+Display:wght@700;900&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg:       #080f0a;
            --panel:    #0d1a10;
            --border:   #1e3a24;
            --green-dim:#1a4a22;
            --green:    #3ddc68;
            --green-hi: #7fffaa;
            --amber:    #f5a623;
            --red:      #ff4d4d;
            --text:     #c8e6c9;
            --muted:    #4a7a55;
            --accent:   {color};
            --font-display: 'Playfair Display', serif;
            --font-mono:    'DM Mono', monospace;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: var(--bg);
            color: var(--text);
            font-family: var(--font-mono);
            min-height: 100vh;
            overflow-x: hidden;
            position: relative;
        }}
        body::before {{
            content: '';
            position: fixed; inset: 0;
            background:
                radial-gradient(ellipse 60% 50% at 20% 30%, rgba(30,100,50,.18) 0%, transparent 70%),
                radial-gradient(ellipse 50% 60% at 80% 70%, rgba(10,60,25,.25) 0%, transparent 65%);
            pointer-events: none;
        }}
        body::after {{
            content: '';
            position: fixed; inset: 0;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
            opacity: .4;
            pointer-events: none;
        }}
        .wrapper {{
            position: relative; z-index: 1;
            max-width: 900px;
            margin: 0 auto;
            padding: 48px 24px 80px;
        }}
        header {{
            display: flex;
            align-items: center;
            gap: 18px;
            margin-bottom: 56px;
            animation: fadeDown .6s ease both;
        }}
        .leaf-icon {{
            width: 52px; height: 52px;
            display: grid; place-items: center;
            background: var(--green-dim);
            border: 1px solid var(--border);
            border-radius: 14px;
            font-size: 28px;
            flex-shrink: 0;
            box-shadow: 0 0 20px rgba(61,220,104,.12);
        }}
        .header-text h1 {{
            font-family: var(--font-display);
            font-size: clamp(1.4rem, 4vw, 2rem);
            font-weight: 900;
            color: var(--green-hi);
            letter-spacing: -.02em;
            line-height: 1.1;
        }}
        .header-text p {{
            font-size: .72rem;
            color: var(--muted);
            letter-spacing: .12em;
            text-transform: uppercase;
            margin-top: 4px;
        }}
        .live-badge {{
            margin-left: auto;
            display: flex; align-items: center; gap: 7px;
            padding: 6px 14px;
            border: 1px solid var(--border);
            border-radius: 999px;
            font-size: .68rem;
            letter-spacing: .1em;
            color: var(--green);
            text-transform: uppercase;
        }}
        .live-dot {{
            width: 7px; height: 7px;
            border-radius: 50%;
            background: var(--green);
            animation: pulse 1.4s ease-in-out infinite;
        }}
        .grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-bottom: 16px;
        }}
        .card {{
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 28px 28px 24px;
            position: relative;
            overflow: hidden;
            animation: fadeUp .6s ease both;
        }}
        .card:nth-child(2) {{ animation-delay: .08s; }}
        .card::before {{
            content: '';
            position: absolute; top: 0; left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--green-dim), transparent);
        }}
        .card-label {{
            font-size: .65rem;
            letter-spacing: .18em;
            text-transform: uppercase;
            color: var(--muted);
            margin-bottom: 16px;
        }}
        .card-icon {{
            font-size: 1.8rem;
            margin-bottom: 10px;
            display: block;
        }}
        .card-value {{
            font-family: var(--font-display);
            font-size: clamp(2.8rem, 6vw, 3.8rem);
            font-weight: 900;
            line-height: 1;
            color: var(--green-hi);
        }}
        .card-unit {{
            font-family: var(--font-mono);
            font-size: 1rem;
            color: var(--muted);
            font-weight: 300;
            margin-left: 4px;
        }}
        .sparkline {{
            display: flex; align-items: flex-end;
            gap: 3px; height: 28px; margin-top: 16px;
        }}
        .bar {{
            flex: 1; border-radius: 3px 3px 0 0;
            background: var(--green-dim);
            opacity: .6;
            animation: barGrow .8s ease both;
        }}
        .bar:last-child {{ background: var(--green); opacity: 1; }}
        .risk-card {{ grid-column: 1 / -1; animation-delay: .16s; }}
        .risk-header {{
            display: flex; align-items: center; justify-content: space-between;
            margin-bottom: 20px;
        }}
        .risk-value-wrap {{
            display: flex; align-items: baseline; gap: 8px;
        }}
        .risk-value {{
            font-family: var(--font-display);
            font-size: clamp(3rem, 8vw, 5rem);
            font-weight: 900;
            line-height: 1;
            color: var(--accent);
        }}
        .risk-label-big {{
            font-size: 1.1rem;
            font-weight: 500;
            color: var(--accent);
            opacity: .8;
        }}
        .progress-track {{
            height: 10px;
            background: var(--green-dim);
            border-radius: 999px;
            overflow: visible;
            margin-top: 18px;
            position: relative;
        }}
        .progress-fill {{
            height: 100%;
            width: {risk}%;
            background: linear-gradient(90deg, var(--green), var(--accent));
            border-radius: 999px;
            position: relative;
        }}
        .progress-fill::after {{
            content: '';
            position: absolute; right: 0; top: 50%;
            transform: translate(50%, -50%);
            width: 14px; height: 14px;
            border-radius: 50%;
            background: var(--accent);
            box-shadow: 0 0 10px var(--accent);
        }}
        .ticks {{
            display: flex; justify-content: space-between;
            margin-top: 8px;
            font-size: .6rem;
            color: var(--muted);
            letter-spacing: .05em;
        }}
        .status-banner {{
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 16px 22px;
            display: flex; align-items: center; gap: 14px;
            background: rgba(13,26,16,.7);
            animation: fadeUp .6s .28s ease both;
            margin-top: 16px;
        }}
        .status-icon {{ font-size: 1.5rem; flex-shrink: 0; }}
        .status-text strong {{
            display: block;
            font-size: .88rem;
            color: var(--accent);
            margin-bottom: 2px;
        }}
        .status-text span {{
            font-size: .72rem;
            color: var(--muted);
        }}
        footer {{
            margin-top: 48px;
            display: flex; justify-content: space-between; align-items: center;
            font-size: .65rem;
            color: var(--muted);
            letter-spacing: .1em;
            text-transform: uppercase;
            animation: fadeUp .6s .36s ease both;
            border-top: 1px solid var(--border);
            padding-top: 20px;
        }}
        @keyframes fadeDown {{
            from {{ opacity: 0; transform: translateY(-16px); }}
            to   {{ opacity: 1; transform: translateY(0); }}
        }}
        @keyframes fadeUp {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to   {{ opacity: 1; transform: translateY(0); }}
        }}
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; box-shadow: 0 0 0 0 rgba(61,220,104,.5); }}
            50%       {{ opacity: .6; box-shadow: 0 0 0 5px transparent; }}
        }}
        @keyframes barGrow {{
            from {{ transform: scaleY(0); transform-origin: bottom; }}
            to   {{ transform: scaleY(1); }}
        }}
        @media (max-width: 520px) {{
            .grid {{ grid-template-columns: 1fr; }}
            .risk-card {{ grid-column: 1; }}
            .live-badge {{ display: none; }}
        }}
    </style>
</head>
<body>
<div class="wrapper">

    <header>
        <div class="leaf-icon">🍓</div>
        <div class="header-text">
            <h1>Mildew Monitor</h1>
            <p>Strawberry crop — live sensor feed</p>
        </div>
        <div class="live-badge">
            <span class="live-dot"></span>
            Live
        </div>
    </header>

    <div class="grid">

        <div class="card">
            <span class="card-icon">🌡</span>
            <div class="card-label">Temperature</div>
            <div>
                <span class="card-value">{temp}</span>
                <span class="card-unit">°C</span>
            </div>
            <div class="sparkline">
                <div class="bar" style="height:40%"></div>
                <div class="bar" style="height:55%"></div>
                <div class="bar" style="height:45%"></div>
                <div class="bar" style="height:65%"></div>
                <div class="bar" style="height:50%"></div>
                <div class="bar" style="height:70%"></div>
                <div class="bar" style="height:60%"></div>
                <div class="bar" style="height:75%"></div>
                <div class="bar" style="height:80%"></div>
                <div class="bar" style="height:100%"></div>
            </div>
        </div>

        <div class="card">
            <span class="card-icon">💧</span>
            <div class="card-label">Humidity</div>
            <div>
                <span class="card-value">{hum}</span>
                <span class="card-unit">%</span>
            </div>
            <div class="sparkline">
                <div class="bar" style="height:60%"></div>
                <div class="bar" style="height:70%"></div>
                <div class="bar" style="height:65%"></div>
                <div class="bar" style="height:80%"></div>
                <div class="bar" style="height:75%"></div>
                <div class="bar" style="height:85%"></div>
                <div class="bar" style="height:78%"></div>
                <div class="bar" style="height:90%"></div>
                <div class="bar" style="height:82%"></div>
                <div class="bar" style="height:100%"></div>
            </div>
        </div>

        <div class="card risk-card">
            <div class="risk-header">
                <div>
                    <div class="card-label">Mildew Risk Index</div>
                    <div class="risk-value-wrap">
                        <span class="risk-value">{risk}</span>
                        <span class="card-unit" style="font-size:1.6rem">/100</span>
                    </div>
                </div>
                <span class="risk-label-big" id="risk-label"></span>
            </div>
            <div class="progress-track">
                <div class="progress-fill"></div>
            </div>
            <div class="ticks">
                <span>0 — Safe</span>
                <span>25</span>
                <span>50 — Moderate</span>
                <span>75</span>
                <span>100 — Critical</span>
            </div>
        </div>

    </div>

    <div class="status-banner">
        <div class="status-icon" id="status-icon"></div>
        <div class="status-text">
            <strong id="status-title"></strong>
            <span id="status-msg"></span>
        </div>
    </div>

    <footer>
        <span>Live GPIO · No CSV</span>
        <span>Auto-refresh every 3 s</span>
        <span id="ts"></span>
    </footer>

</div>
<script>
    const risk = {risk};
    let label, icon, title, msg;
    if (risk >= 80) {{
        label = "⚠ Critical";
        icon  = "🚨";
        title = "High Mildew Risk — Act Now";
        msg   = "Conditions are highly favourable for powdery mildew. Consider fungicide application.";
    }} else if (risk >= 50) {{
        label = "⚠ Moderate";
        icon  = "⚠️";
        title = "Elevated Risk Detected";
        msg   = "Monitor closely. Conditions may worsen — check again in 30 minutes.";
    }} else {{
        label = "✓ Low";
        icon  = "✅";
        title = "Conditions Normal";
        msg   = "No significant fungal risk detected. Continue routine monitoring.";
    }}
    document.getElementById("risk-label").textContent  = label;
    document.getElementById("status-icon").textContent = icon;
    document.getElementById("status-title").textContent = title;
    document.getElementById("status-msg").textContent  = msg;
    document.getElementById("ts").textContent =
        new Date().toLocaleTimeString("en-GB", {{hour:"2-digit", minute:"2-digit", second:"2-digit"}});
</script>
</body>
</html>
"""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)