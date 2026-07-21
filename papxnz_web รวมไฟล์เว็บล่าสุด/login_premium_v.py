from __future__ import annotations

import json
import os
from html import escape
from urllib.parse import urlencode

from fastapi.responses import HTMLResponse

try:
    from packages_v import MAIN_WEB_LINK, PUBLIC_PACKAGES_LINK, _login_provider_config
except Exception:
    MAIN_WEB_LINK = "https://papxnzvip.com/"
    PUBLIC_PACKAGES_LINK = "/packages"

    def _login_provider_config() -> dict[str, str]:
        return {
            # Client ID is public and goes to the browser.  The secret stays
            # server-only in TELEGRAM_LOGIN_CLIENT_SECRET.
            "telegram_client_id": os.getenv("TELEGRAM_LOGIN_CLIENT_ID", "8806048880"),
            "telegram_redirect_uri": os.getenv("TELEGRAM_LOGIN_REDIRECT_URI", "https://papxnzvip.com/packages"),
            "google_client_id": "",
            "google_redirect_uri": "",
            "telegram_confirm_link": "",
        }


def login_page(*, mode: str = "login", next_url: str = "/packages") -> HTMLResponse:
    initial_mode = "register" if str(mode or "").lower() == "register" else "login"
    safe_next = str(next_url or "/packages")
    if not safe_next.startswith("/") or safe_next.startswith("//"):
        safe_next = "/packages"

    provider_config = _login_provider_config()
    telegram_client_id = str(provider_config.get("telegram_client_id") or "").strip()
    telegram_redirect_uri = str(provider_config.get("telegram_redirect_uri") or "").strip()
    google_client_id = str(provider_config.get("google_client_id") or "").strip()
    google_redirect_uri = str(provider_config.get("google_redirect_uri") or "").strip()

    js_config = {
        "mode": initial_mode,
        "nextUrl": safe_next,
        "packagesUrl": PUBLIC_PACKAGES_LINK,
        "successUrl": MAIN_WEB_LINK,
        "telegramClientId": telegram_client_id,
        "telegramRedirectUri": telegram_redirect_uri,
        "googleClientId": google_client_id,
        "googleRedirectUri": google_redirect_uri,
    }

    content = """<!doctype html>
<html lang="th">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>PAPXNZ Premium Login</title>
  <style>
    @font-face{font-family:Kanit;src:url("/static/fonts/Kanit-400.ttf") format("truetype");font-weight:400;font-display:swap}
    @font-face{font-family:Kanit;src:url("/static/fonts/Kanit-600.ttf") format("truetype");font-weight:600;font-display:swap}
    @font-face{font-family:Kanit;src:url("/static/fonts/Kanit-800.ttf") format("truetype");font-weight:800;font-display:swap}
    :root{
      color-scheme:dark;
      --bg:#070910;
      --panel:#0d1014;
      --gold:#e0aa3e;
      --gold-2:#fff1b3;
      --gold-3:#d89416;
      --text:#fff8e8;
      --muted:rgba(255,247,225,.68);
      --line:rgba(255,230,158,.30);
      --danger:#ff8178;
      --telegram:#229ed9;
    }
    *{box-sizing:border-box}
    html,body{margin:0;min-height:100%;background:var(--bg);color:var(--text);font-family:Kanit,"Noto Sans Thai","Segoe UI",sans-serif;letter-spacing:0}
    button,input{font:inherit}
    body{
      overflow-x:hidden;
      background:
        radial-gradient(circle at 50% -12%, rgba(255,244,188,.20), rgba(224,170,62,.08) 28%, transparent 58%),
        radial-gradient(circle at 18% 20%, rgba(86,145,178,.13), transparent 30%),
        radial-gradient(circle at 84% 76%, rgba(224,170,62,.13), transparent 33%),
        linear-gradient(180deg,#090b12 0%,#05070c 58%,#030408 100%);
    }
    .page{
      min-height:100dvh;
      padding:0;
      display:grid;
      place-items:stretch center;
    }
    .card{
      width:100%;
      max-width:560px;
      min-height:100dvh;
      position:relative;
      overflow:hidden;
      border:1px solid rgba(255,231,156,.74);
      border-top:0;
      border-bottom:0;
      border-radius:0;
      padding:36px clamp(22px,6vw,34px) max(24px,env(safe-area-inset-bottom));
      background:
        linear-gradient(135deg,rgba(255,244,190,.13),transparent 24%),
        linear-gradient(215deg,rgba(109,160,188,.18),transparent 30%),
        radial-gradient(circle at 50% 8%,rgba(255,241,177,.25),transparent 18%),
        radial-gradient(circle at 18% 2%,rgba(228,154,32,.28),transparent 26%),
        linear-gradient(180deg,rgba(23,27,29,.94),rgba(8,10,12,.97) 48%,rgba(7,8,10,.99));
      box-shadow:0 24px 70px rgba(0,0,0,.60),0 0 36px rgba(224,170,62,.22),inset 0 1px 0 rgba(255,255,255,.16);
    }
    .card:before,.card:after{content:"";position:absolute;pointer-events:none}
    .card:before{
      inset:0;
      background:
        linear-gradient(112deg,transparent 0 18%,rgba(255,232,157,.20) 20%,transparent 23% 76%,rgba(255,255,255,.14) 78%,transparent 81%),
        linear-gradient(18deg,transparent 0 60%,rgba(255,221,132,.12) 63%,transparent 66%);
      opacity:.56;
    }
    .card:after{
      left:12%;right:12%;bottom:-34px;height:74px;border-radius:999px;
      background:rgba(224,170,62,.24);filter:blur(28px);
    }
    .inner{position:relative;z-index:1;min-height:calc(100dvh - 60px);display:flex;flex-direction:column;align-items:center;text-align:center}
    .crown{height:32px;margin:0 0 6px;color:#fff0b5;font-size:28px;line-height:1;text-shadow:0 0 18px rgba(255,229,147,.48)}
    h1{
      margin:0;
      font-size:48px;
      line-height:.96;
      font-weight:800;
      color:transparent;
      background:linear-gradient(180deg,#fff7c8 0%,#f4d775 34%,#b98225 72%,#fff1ad 100%);
      -webkit-background-clip:text;background-clip:text;
      filter:drop-shadow(0 0 16px rgba(255,224,135,.22));
    }
    .kicker{margin-top:8px;color:rgba(255,239,190,.82);font-size:12px;font-weight:600;letter-spacing:3px}
    .headline{margin:22px 0 7px;color:#fff6df;font-size:25px;line-height:1.25;font-weight:600}
    .sub{margin:0;color:var(--muted);font-size:14px;line-height:1.45;font-weight:400}
    .promo-card{
      --promo-overlay-image:none;
      width:100%;
      margin:28px 0 0;
      min-height:clamp(245px,36dvh,360px);
      flex:0 0 auto;
      position:relative;
      overflow:hidden;
      border:1px solid rgba(255,236,170,.46);
      border-radius:24px;
      padding:22px 22px;
      text-align:left;
      background:
        radial-gradient(circle at 82% 18%,rgba(255,232,153,.18),transparent 30%),
        linear-gradient(135deg,rgba(255,241,188,.14),transparent 42%),
        linear-gradient(180deg,rgba(255,255,255,.060),rgba(255,255,255,.026)),
        rgba(8,10,12,.64);
      box-shadow:inset 0 1px 0 rgba(255,255,255,.10),0 18px 34px rgba(0,0,0,.30),0 0 24px rgba(224,170,62,.10);
    }
    .promo-card:before{
      content:"";
      position:absolute;
      inset:0;
      background-image:var(--promo-overlay-image);
      background-size:cover;
      background-position:center;
      opacity:.22;
      mix-blend-mode:screen;
      pointer-events:none;
    }
    .promo-card:after{
      content:"";
      position:absolute;
      inset:0;
      background:linear-gradient(90deg,rgba(5,7,10,.82),rgba(5,7,10,.42) 62%,rgba(255,222,128,.10));
      pointer-events:none;
    }
    .promo-card > *{position:relative;z-index:1}
    .promo-label{display:inline-flex;min-height:26px;align-items:center;border-radius:999px;padding:0 12px;color:#1d1407;background:linear-gradient(90deg,#fff1b7,#e0aa3e);font-size:11px;font-weight:700}
    .promo-title{max-width:82%;margin:18px 0 7px;color:#fff5d7;font-size:24px;line-height:1.18;font-weight:600}
    .promo-copy{max-width:78%;margin:0;color:rgba(255,244,214,.72);font-size:14px;line-height:1.48}
    .action-zone{
      width:100%;
      margin-top:0;
      padding-top:24px;
      display:flex;
      flex-direction:column;
      align-items:center;
    }
    .signup-label{
      margin:0 0 14px;
      color:rgba(255,245,220,.72);
      font-size:14px;
      line-height:1.25;
      font-weight:500;
    }
    .channel-row{
      width:100%;
      display:grid;
      grid-template-columns:1fr 1fr;
      gap:12px;
    }
    .channel-btn{
      width:100%;
      min-height:58px;
      display:flex;
      align-items:center;
      justify-content:center;
      gap:10px;
      border:1px solid rgba(255,246,208,.88);
      border-radius:20px;
      font-size:14px;
      font-weight:600;
      cursor:pointer;
      transition:transform .16s ease,box-shadow .16s ease,filter .16s ease;
    }
    .channel-btn:hover{transform:translateY(-1px);filter:saturate(1.05)}
    .channel-btn:active{transform:translateY(0)}
    .channel-btn.telegram{
      color:#f5fbff;
      border-color:rgba(139,212,255,.56);
      background:
        linear-gradient(180deg,rgba(255,255,255,.22),rgba(255,255,255,.035) 44%,rgba(0,0,0,.12) 45%),
        radial-gradient(circle at 24% 18%,rgba(255,241,183,.28),transparent 28%),
        linear-gradient(135deg,#31aaf2 0%,#1682c7 42%,#0b467a 100%);
      box-shadow:0 0 0 5px rgba(34,158,217,.10),0 0 24px rgba(34,158,217,.30),0 12px 24px rgba(0,0,0,.30),inset 0 1px 0 rgba(255,255,255,.36);
    }
    .channel-btn.google{
      color:#151515;
      border-color:rgba(255,255,255,.86);
      background:
        linear-gradient(180deg,rgba(255,255,255,.95),rgba(255,249,229,.88)),
        #fff;
      box-shadow:0 0 0 5px rgba(255,255,255,.06),0 12px 24px rgba(0,0,0,.28),inset 0 1px 0 rgba(255,255,255,.95);
    }
    .tg-icon,.gg-icon{width:32px;height:32px;flex:0 0 32px;border-radius:50%;display:grid;place-items:center;box-shadow:0 6px 14px rgba(0,0,0,.18)}
    .tg-icon{background:var(--telegram)}
    .gg-icon{background:#fff}
    .tg-icon svg,.gg-icon svg{width:32px;height:32px;display:block}
    .points{width:100%;margin-top:16px;display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
    .point{min-width:0;display:flex;flex-direction:column;align-items:center;gap:8px;color:rgba(255,242,202,.86);font-size:13px;line-height:1.2}
    .point-mark{width:36px;height:36px;display:grid;place-items:center;border:1px solid rgba(255,236,170,.66);border-radius:50%;color:#ffdf7e;background:rgba(255,255,255,.035);box-shadow:inset 0 1px 0 rgba(255,255,255,.08),0 0 16px rgba(224,170,62,.10);font-size:18px}
    .board-note{
      width:100%;
      margin-top:18px;
      padding:14px 0 0;
      border-top:1px solid rgba(255,236,170,.10);
      display:grid;
      grid-template-columns:repeat(3,1fr);
      gap:8px;
      color:rgba(255,241,207,.58);
      text-align:center;
    }
    .note-item{
      min-width:0;
      display:grid;
      gap:3px;
      padding:0 4px;
    }
    .note-item b{
      color:rgba(255,247,225,.82);
      font-size:13px;
      line-height:1.15;
      font-weight:600;
    }
    .note-item span{
      font-size:10.5px;
      line-height:1.2;
      white-space:nowrap;
      overflow:hidden;
      text-overflow:ellipsis;
    }
    .create-copy{width:100%;margin-top:18px;padding-top:16px;border-top:1px solid rgba(255,236,170,.12);display:flex;align-items:center;justify-content:center;gap:9px;color:rgba(255,241,207,.50);font-size:12px;line-height:1.2}
    .create-btn{min-height:30px;border:1px solid rgba(255,236,170,.18);border-radius:999px;padding:0 13px;color:rgba(255,241,207,.74);background:rgba(255,255,255,.026);backdrop-filter:blur(8px);font-size:12px;font-weight:500;cursor:pointer}
    .create-btn:hover{border-color:rgba(255,236,170,.34);background:rgba(255,255,255,.045);color:rgba(255,247,225,.90)}
    .powered{margin-top:16px;color:rgba(255,245,218,.54);font-size:10px;text-transform:uppercase}
    .drawer{
      position:fixed;
      inset:0;
      z-index:20;
      display:none;
      align-items:flex-end;
      justify-content:center;
      padding:16px;
      background:rgba(2,3,6,.72);
      backdrop-filter:blur(14px);
    }
    .drawer[data-open=true]{display:flex}
    .sheet{
      width:min(100%,430px);
      border:1px solid rgba(255,231,156,.36);
      border-radius:22px;
      padding:18px;
      background:radial-gradient(circle at 50% 0,rgba(255,230,150,.16),transparent 30%),linear-gradient(180deg,rgba(20,23,25,.98),rgba(8,10,12,.99));
      box-shadow:0 24px 70px rgba(0,0,0,.64),0 0 28px rgba(224,170,62,.14);
    }
    .sheet-head{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:14px}
    .sheet-title{font-size:18px;font-weight:600;color:#fff6df}
    .close{width:36px;height:36px;border:1px solid rgba(255,236,170,.18);border-radius:50%;background:rgba(255,255,255,.045);color:#fff3cf;cursor:pointer}
    .field{display:grid;gap:6px;margin-top:12px;text-align:left}
    .field label{color:rgba(255,242,211,.72);font-size:12px}
    .field input{width:100%;height:46px;border:1px solid rgba(255,236,170,.18);border-radius:14px;background:rgba(255,255,255,.055);color:#fff8e8;padding:0 14px;outline:none}
    .field input:focus{border-color:rgba(255,231,156,.58);box-shadow:0 0 0 3px rgba(224,170,62,.12)}
    .primary{width:100%;height:48px;margin-top:14px;border:0;border-radius:14px;background:linear-gradient(90deg,#fff0b7,#e0aa3e,#fff1b7);color:#181004;font-weight:700;cursor:pointer}
    .secondary{width:100%;height:44px;margin-top:10px;border:1px solid rgba(255,236,170,.18);border-radius:14px;background:rgba(255,255,255,.045);color:#fff1cf;cursor:pointer}
    .status{min-height:20px;margin-top:12px;color:rgba(255,242,211,.78);font-size:12.5px;line-height:1.45;text-align:left}
    .status[data-kind=error]{color:var(--danger)}
    .status[data-kind=ok]{color:#bff3c6}
    /* Registration popup only: the main login palette is unchanged. */
    .register-row{display:none;text-align:center;padding:10px 4px 4px}
    .register-row h2{margin:4px 0 8px;color:#efd85c;font-size:32px;font-weight:800}
    .register-row p{margin:0;color:rgba(255,246,218,.72);font-size:14px;line-height:1.5}
    .register-platform{width:100%;min-height:58px;margin-top:30px;border:1px solid rgba(151,216,255,.58);border-radius:999px;color:#fff;background:linear-gradient(135deg,#32aaf0,#3e49db);font-size:17px;font-weight:600;cursor:pointer}
    .register-foot{margin-top:20px;padding-top:16px;border-top:1px solid rgba(255,236,170,.24);color:rgba(255,243,206,.58);font-size:12px}
    .sheet[data-view=register]{padding:30px 26px 24px;border-radius:34px;background:radial-gradient(circle at 0 0,rgba(226,211,105,.20),transparent 38%),linear-gradient(145deg,rgba(48,49,34,.98),rgba(14,16,12,.99))}
    .sheet[data-view=register] .telegram-row,.sheet[data-view=register] .secondary{display:none}
    .sheet[data-view=register] .register-row{display:block}
    .form-row{display:none}
    @media (min-width:680px){
      .page{padding:18px}
      .card{min-height:calc(100dvh - 36px);border:1px solid rgba(255,231,156,.74);border-radius:30px}
      .inner{min-height:0}
    }
    @media (max-width:420px){
      .card{min-height:100dvh;padding:30px 20px max(22px,env(safe-area-inset-bottom))}
      .inner{min-height:0}
      h1{font-size:42px}
      .headline{margin-top:20px;font-size:22px}
      .promo-card{margin-top:24px;min-height:clamp(245px,36dvh,340px);padding:20px}
      .promo-title{font-size:21px}
      .promo-copy{font-size:13px}
      .action-zone{padding-top:22px}
      .channel-row{gap:10px}
      .channel-btn{min-height:56px;border-radius:18px;font-size:13px}
      .tg-icon,.gg-icon{width:30px;height:30px;flex-basis:30px}
      .tg-icon svg,.gg-icon svg{width:30px;height:30px}
      .board-note{grid-template-columns:1fr 1fr 1fr;gap:5px}
      .note-item b{font-size:12px}
      .note-item span{font-size:10px}
    }
  </style>
</head>
<body>
  <main class="page">
    <section class="card" aria-labelledby="loginTitle">
      <div class="inner">
        <div class="crown" aria-hidden="true">♕</div>
        <h1 id="loginTitle">PAPXNZ</h1>
        <div class="kicker">PREMIUM ACCESS</div>
        <p class="headline">เข้าสู่ระบบด้วย Telegram</p>
        <p class="sub">ปลอดภัย · รวดเร็ว · เชื่อถือได้</p>
        <article class="promo-card" id="promoCard" data-editable-promo="true" data-overlay-src="">
          <span class="promo-label">PROMOTION</span>
          <h2 class="promo-title">VIP Access พร้อมใช้งานทันที</h2>
          <p class="promo-copy">สิทธิ์พิเศษสำหรับสมาชิก VIP พร้อมประสบการณ์เข้าถึงที่รวดเร็ว ปลอดภัย และดูแลง่ายกว่าเดิม</p>
        </article>
        <div class="action-zone">
          <p class="signup-label">สมัครบัญชีผ่านช่องทาง</p>
          <div class="channel-row" aria-label="Signup channels">
            <button class="channel-btn telegram" id="telegramMain" type="button">
              <span class="tg-icon" aria-hidden="true">
                <svg viewBox="0 0 24 24" focusable="false">
                  <circle cx="12" cy="12" r="12" fill="#229ED9"></circle>
                  <path fill="#fff" d="M17.42 7.22 5.98 11.64c-.78.31-.77.74-.14.93l2.92.91 1.12 3.52c.14.39.07.54.48.54.36 0 .52-.16.72-.35l1.73-1.68 3.6 2.66c.66.36 1.13.17 1.29-.61l2.34-11.02c.24-.94-.36-1.37-.98-1.12zM9.24 13.27l6.67-4.21c.33-.2.63-.09.38.13l-5.7 5.15-.22 2.32-1.13-3.39z"></path>
                </svg>
              </span>
              <span>Telegram</span>
            </button>
            <button class="channel-btn google" id="googleBtn" type="button">
              <span class="gg-icon" aria-hidden="true">
                <svg viewBox="0 0 48 48" focusable="false">
                  <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"></path>
                  <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"></path>
                  <path fill="#FBBC05" d="M10.53 28.59a14.5 14.5 0 0 1 0-9.18l-7.98-6.19a23.99 23.99 0 0 0 0 21.56l7.98-6.19z"></path>
                  <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"></path>
                </svg>
              </span>
              <span>Google</span>
            </button>
          </div>
          <div class="create-copy">
            <span>หรือสร้างบัญชี</span>
            <button type="button" class="create-btn" id="createAccountBtn">สร้างบัญชี</button>
          </div>
          <div class="points" aria-label="Trust badges">
            <div class="point"><span class="point-mark">⌑</span><span>ปลอดภัย</span></div>
            <div class="point"><span class="point-mark">ϟ</span><span>รวดเร็ว</span></div>
            <div class="point"><span class="point-mark">✓</span><span>เชื่อถือได้</span></div>
          </div>
          <div class="board-note" aria-label="Site quick stats">
            <div class="note-item"><b>@papxnz</b><span>ติดต่อแอดมิน</span></div>
            <div class="note-item"><b>128K+</b><span>ยอดเข้าชม</span></div>
            <div class="note-item"><b>0.8s</b><span>ระดับความไว</span></div>
          </div>
          <div class="powered">Powered by PAPXNZ</div>
        </div>
      </div>
    </section>
  </main>

  <section class="drawer" id="drawer" data-open="false" aria-hidden="true">
    <div class="sheet" id="sheet" data-view="telegram" role="dialog" aria-modal="true" aria-labelledby="sheetTitle">
      <div class="sheet-head">
        <div class="sheet-title" id="sheetTitle">ยืนยัน Telegram</div>
        <button class="close" id="closeDrawer" type="button" aria-label="ปิด">×</button>
      </div>
      <div class="telegram-row">
        <div class="field">
          <label>Telegram</label>
          <input type="text" value="ยืนยันตัวตนกับ Telegram official" readonly aria-label="Telegram OpenID">
        </div>
        <button class="primary" id="telegramConfirm" type="button">ยืนยันใน Telegram official</button>
      </div>
      <div class="register-row">
        <h2>สมัครบัญชี</h2>
        <p>สร้างบัญชีใหม่เพื่อเติมเงิน ซื้อแพ็กเกจ<br>และดูยอดคงเหลือของคุณ</p>
        <button class="register-platform" id="registerTelegram" type="button">สร้างบัญชีด้วย Telegram</button>
        <div class="register-foot">Telegram official จะยืนยันตัวตนและสร้างบัญชีให้ทันที</div>
      </div>
      <button class="secondary" id="backTelegram" type="button">กลับไป Telegram</button>
      <div class="status" id="status" aria-live="polite"></div>
    </div>
  </section>

  <script>
    window.PAPXNZ_LOGIN_CONFIG = __CONFIG__;
  </script>
  <script>
  (() => {
    const cfg = window.PAPXNZ_LOGIN_CONFIG || {};
    const drawer = document.getElementById('drawer');
    const sheet = document.getElementById('sheet');
    const status = document.getElementById('status');
    const promoCard = document.getElementById('promoCard');
    const sessionKey = 'papxnz_packages_session_id';
    const userKey = 'papxnz_packages_user';
    const fingerprintKey = 'papxnz_ui_fingerprint_id';
    const tgStateKey = 'papxnz_telegram_openid_state';
    const tgVerifierKey = 'papxnz_telegram_openid_verifier';
    const tgRedirectKey = 'papxnz_telegram_openid_redirect';
    const googleStateKey = 'papxnz_google_openid_state';
    const googleNonceKey = 'papxnz_google_openid_nonce';
    const googleRedirectKey = 'papxnz_google_openid_redirect';
    let mode = cfg.mode || 'login';
    if (new URLSearchParams(location.search).get('telegram_callback') === '1') {
      cfg.nextUrl = localStorage.getItem('papxnz_telegram_return_next') || cfg.nextUrl;
      mode = localStorage.getItem('papxnz_telegram_return_mode') || mode;
    }
    const promoOverlay = promoCard?.dataset.overlaySrc || cfg.promoOverlay || '';
    if (promoCard && promoOverlay) {
      promoCard.style.setProperty('--promo-overlay-image', `url("${promoOverlay}")`);
    }

    const openDrawer = (view = 'telegram') => {
      sheet.dataset.view = view;
      document.getElementById('sheetTitle').textContent = view === 'register' ? 'สร้างบัญชี PAPXNZ' : 'ยืนยัน Telegram';
      drawer.dataset.open = 'true';
      drawer.setAttribute('aria-hidden', 'false');
      status.textContent = '';
      status.dataset.kind = '';
    };
    const closeDrawer = () => {
      drawer.dataset.open = 'false';
      drawer.setAttribute('aria-hidden', 'true');
    };
    const setStatus = (message, kind = '') => {
      status.textContent = message || '';
      status.dataset.kind = kind;
    };
    const sessionId = (() => {
      let current = localStorage.getItem(sessionKey);
      if (!current) {
        current = `web_${Date.now()}_${Math.random().toString(36).slice(2, 10)}`;
        localStorage.setItem(sessionKey, current);
      }
      return current;
    })();
    const fingerprintId = () => {
      let current = localStorage.getItem(fingerprintKey);
      if (!current) {
        current = `fp_${Date.now()}_${Math.random().toString(36).slice(2, 12)}`;
        localStorage.setItem(fingerprintKey, current);
      }
      return current;
    };
    const uiTrace = () => ({
      ui_fingerprint_id: fingerprintId(),
      ui_session_id: sessionId,
      ui_saved_user: localStorage.getItem(userKey) || '',
      ui_path: location.pathname + location.search,
      ui_timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || '',
      ui_language: navigator.language || '',
      ui_platform: navigator.platform || '',
      ui_screen: `${screen.width}x${screen.height}`,
    });
    const randomHex = (length = 48) => {
      const bytes = new Uint8Array(length);
      crypto.getRandomValues(bytes);
      return Array.from(bytes, (byte) => byte.toString(16).padStart(2, '0')).join('');
    };
    const base64Url = (buffer) => {
      const bytes = new Uint8Array(buffer);
      let binary = '';
      bytes.forEach((byte) => binary += String.fromCharCode(byte));
      return btoa(binary).replace(/[+]/g, '-').replace(/[/]/g, '_').replace(/=+$/g, '');
    };
    const sha256 = async (value) => crypto.subtle.digest('SHA-256', new TextEncoder().encode(value));
    const cleanTelegramRedirectUri = () => {
      if (cfg.telegramRedirectUri) return cfg.telegramRedirectUri;
      const url = new URL(location.href);
      url.pathname = '/login';
      url.hash = '';
      url.search = '';
      return url.toString();
    };
    const cleanGoogleRedirectUri = () => {
      if (cfg.googleRedirectUri) return cfg.googleRedirectUri;
      const url = new URL(location.href);
      url.pathname = '/login';
      url.hash = '';
      url.search = '';
      return url.toString();
    };
    const postAction = async (payload) => {
      const response = await fetch('/customer/action', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'Accept': 'application/json'},
        credentials: 'same-origin',
        body: JSON.stringify({...uiTrace(), ...payload}),
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok || data.ok === false) {
        throw new Error(data.message || data.code || data.detail || 'ทำรายการไม่สำเร็จ');
      }
      return data;
    };
    const buildTelegramUrl = async () => {
      if (!cfg.telegramClientId) throw new Error('ยังไม่ได้ตั้งค่า Telegram client id');
      const state = randomHex(24);
      const verifier = randomHex(48);
      const challenge = base64Url(await sha256(verifier));
      const redirectUri = cleanTelegramRedirectUri();
      localStorage.setItem('papxnz_telegram_return_next', cfg.nextUrl || '/');
      localStorage.setItem('papxnz_telegram_return_mode', mode || 'login');
      localStorage.setItem(tgStateKey, state);
      localStorage.setItem(tgVerifierKey, verifier);
      localStorage.setItem(tgRedirectKey, redirectUri);
      const params = new URLSearchParams({
        response_type: 'code',
        client_id: cfg.telegramClientId,
        redirect_uri: redirectUri,
        scope: 'openid',
        state,
        code_challenge: challenge,
        code_challenge_method: 'S256',
      });
      return `https://oauth.telegram.org/auth?${params.toString()}`;
    };
    const requestTelegram = async () => {
      try {
        setStatus('กำลังเปิด Telegram official...', '');
        location.href = await buildTelegramUrl();
      } catch (err) {
        setStatus(err.message || 'เปิด Telegram ไม่สำเร็จ', 'error');
      }
    };
    const handleTelegramReturn = async () => {
      const params = new URLSearchParams(location.search);
      const code = params.get('code') || '';
      const state = params.get('state') || '';
      const telegramError = params.get('error') || '';
      if (!code && !telegramError) return;
      openDrawer('telegram');
      if (telegramError) {
        setStatus(params.get('error_description') || telegramError, 'error');
        return;
      }
      const expected = localStorage.getItem(tgStateKey) || '';
      const verifier = localStorage.getItem(tgVerifierKey) || '';
      const redirectUri = localStorage.getItem(tgRedirectKey) || cleanTelegramRedirectUri();
      if (!state || state !== expected || !verifier) {
        setStatus('คำตอบ Telegram ไม่ตรงกับคำสั่งเดิม กรุณากดยืนยันใหม่', 'error');
        return;
      }
      setStatus('ได้รับคำตอบจาก Telegram แล้ว กำลังให้ backend ตรวจ...', '');
      try {
        const data = await postAction({
          action: 'auth.telegram.openid_confirm',
          action_key: 'auth.telegram.openid_confirm',
          mode: 'openid_confirm',
          event_type: 'auth.telegram.openid_confirm',
          ui_id: 'ui.auth.telegram_button',
          provider: 'telegram',
          auth_mode: mode,
          session_id: sessionId,
          source: mode === 'register' ? 'register_page' : 'login_page',
          path: location.pathname + location.search,
          code,
          state,
          code_verifier: verifier,
          redirect_uri: redirectUri,
          client_id: cfg.telegramClientId,
        });
        localStorage.removeItem(tgStateKey);
        localStorage.removeItem(tgVerifierKey);
        localStorage.removeItem(tgRedirectKey);
        setStatus(data.message || 'ยืนยัน Telegram สำเร็จ', 'ok');
        setTimeout(() => { location.href = cfg.nextUrl || cfg.successUrl || cfg.packagesUrl; }, 850);
      } catch (err) {
        setStatus(err.message || 'ตรวจ Telegram OpenID ไม่สำเร็จ', 'error');
      }
    };
    const googleLogin = async () => {
      openDrawer('telegram');
      if (!cfg.googleClientId) {
        setStatus('ยังไม่ได้ตั้งค่า Google Client ID', 'error');
        return;
      }
      const state = randomHex(24);
      const nonce = randomHex(24);
      const redirectUri = cleanGoogleRedirectUri();
      localStorage.setItem(googleStateKey, state);
      localStorage.setItem(googleNonceKey, nonce);
      localStorage.setItem(googleRedirectKey, redirectUri);
      setStatus('กำลังเปิดหน้าเลือกบัญชี Google...', '');
      const params = new URLSearchParams({
        client_id: cfg.googleClientId,
        redirect_uri: redirectUri,
        response_type: 'id_token',
        scope: 'openid email profile',
        state,
        nonce,
        prompt: 'select_account',
      });
      location.href = `https://accounts.google.com/o/oauth2/v2/auth?${params.toString()}`;
    };
    const createAccount = () => {
      mode = 'register';
      openDrawer('register');
    };
    const handleGoogleReturn = async () => {
      const hash = new URLSearchParams(String(location.hash || '').replace(/^#/, ''));
      const params = new URLSearchParams(location.search);
      const idToken = hash.get('id_token') || params.get('id_token') || '';
      const state = hash.get('state') || params.get('state') || '';
      const googleError = hash.get('error') || params.get('error') || '';
      if (!idToken && !googleError) return;
      openDrawer('telegram');
      if (googleError) {
        setStatus(hash.get('error_description') || params.get('error_description') || googleError, 'error');
        return;
      }
      const expected = localStorage.getItem(googleStateKey) || '';
      if (!state || state !== expected) {
        setStatus('คำตอบ Google ไม่ตรงกับคำสั่งเดิม กรุณาเลือกบัญชีใหม่', 'error');
        return;
      }
      setStatus('ได้รับคำตอบจาก Google แล้ว กำลังให้ backend ตรวจ...', '');
      try {
        const data = await postAction({
          action: 'auth.google.login',
          action_key: 'auth.google.login',
          event_type: 'auth.google.login',
          ui_id: 'ui.auth.google_button',
          provider: 'google',
          auth_mode: mode,
          session_id: sessionId,
          source: mode === 'register' ? 'register_page' : 'login_page',
          path: location.pathname + location.search,
          token: idToken,
          id_token: idToken,
          credential: idToken,
          state,
          nonce: localStorage.getItem(googleNonceKey) || '',
          redirect_uri: localStorage.getItem(googleRedirectKey) || cleanGoogleRedirectUri(),
          client_id: cfg.googleClientId,
        });
        localStorage.removeItem(googleStateKey);
        localStorage.removeItem(googleNonceKey);
        localStorage.removeItem(googleRedirectKey);
        setStatus(data.message || 'ยืนยัน Google สำเร็จ', 'ok');
        setTimeout(() => { location.href = cfg.nextUrl || cfg.successUrl || cfg.packagesUrl; }, 850);
      } catch (err) {
        setStatus(err.message || 'ตรวจ Google ไม่สำเร็จ', 'error');
      }
    };

    document.getElementById('telegramMain')?.addEventListener('click', () => openDrawer('telegram'));
    document.getElementById('closeDrawer')?.addEventListener('click', closeDrawer);
    document.getElementById('backTelegram')?.addEventListener('click', () => openDrawer('telegram'));
    document.getElementById('telegramConfirm')?.addEventListener('click', requestTelegram);
    document.getElementById('registerTelegram')?.addEventListener('click', requestTelegram);
    document.getElementById('googleBtn')?.addEventListener('click', googleLogin);
    document.getElementById('createAccountBtn')?.addEventListener('click', createAccount);
    drawer?.addEventListener('click', (event) => {
      if (event.target === drawer) closeDrawer();
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') closeDrawer();
    });
    handleTelegramReturn();
    handleGoogleReturn();
  })();
  </script>
</body>
</html>"""
    content = content.replace("__CONFIG__", json.dumps(js_config, ensure_ascii=False).replace("</", "<\\/"))
    content = content.replace("__PACKAGES__", escape(str(PUBLIC_PACKAGES_LINK), quote=True))
    return HTMLResponse(content)
