import streamlit as st

FOOTER_HTML = """
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
<style>
  .injaz-footer{
    direction: rtl; text-align: center; font-family: 'Cairo', system-ui, sans-serif;
    background:#8A1538; color:#fff; border-radius:20px; padding:28px 18px; margin-top:24px;
    box-shadow: 0 8px 24px rgba(0,0,0,.18);
  }
  .injaz-footer .title{font-weight:700; font-size:1.35rem; margin-bottom:.25rem}
  .injaz-footer .vision{font-size:1.05rem; opacity:.95; margin-bottom:.75rem}
  .injaz-footer .sep{width:210px; height:3px; background:#C9A227; border-radius:2px; margin:14px auto}
  .injaz-footer .row{font-size:1rem; line-height:1.9}
  .injaz-footer .label{color:#C9A227; font-weight:600}
  .injaz-footer a{color:#C9A227; text-decoration:none; font-weight:600; border-bottom:1px dotted rgba(201,162,39,.35)}
  .injaz-footer a:hover{color:#E5C75A; border-bottom:1px solid #E5C75A}
  .injaz-footer .fine{font-size:.92rem; opacity:.95; margin-top:10px}

  /* زر لينكدإن */
  .social{
    display:flex; align-items:center; gap:8px; justify-content:center;
    margin-top:2px;
  }
  .btn-li{
    display:inline-flex; align-items:center; justify-content:center;
    width:32px; height:32px; border-radius:8px; background:#C9A2271a;
    border:1px solid rgba(201,162,39,.45); transition:.2s ease;
  }
  .btn-li:hover{ background:#C9A22733; border-color:#E5C75A }
  .btn-li svg{ width:18px; height:18px; }
  .btn-li svg path{ fill:#C9A227; transition:.2s ease; }
  .btn-li:hover svg path{ fill:#E5C75A; }

  @media (max-width:540px){
    .injaz-footer{padding:22px 14px}
    .injaz-footer .sep{width:160px}
  }
</style>

<div class="injaz-footer">
  <div class="title">🎯 رؤيتنا</div>
  <div class="vision">"متعلّم ريادي لتنمية مستدامة"</div>

  <div class="sep"></div>

  <div class="row"><span class="label">منسّق المشاريع الإلكترونية:</span> أ. سحر عثمان</div>
  <div class="row">📧 <a href="mailto:Sahar.Osman@education.qa">Sahar.Osman@education.qa</a></div>

  <div class="row social">
    <a class="btn-li" href="https://www.linkedin.com/in/sahar-osman-a19a45209/" target="_blank" rel="noopener" aria-label="LinkedIn">
      <!-- أيقونة LinkedIn رسمية (SVG) -->
      <svg viewBox="0 0 24 24" role="img" aria-hidden="true">
        <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.447-2.136 2.942v5.664H9.35V9h3.414v1.561h.049c.476-.9 1.637-1.852 3.367-1.852 3.6 0 4.262 2.37 4.262 5.455v6.288zM5.337 7.433a2.062 2.062 0 1 1 0-4.124 2.062 2.062 0 0 1 0 4.124zM7.114 20.452H3.56V9h3.554v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.225.792 24 1.771 24h20.451C23.2 24 24 23.225 24 22.271V1.729C24 .774 23.2 0 22.225 0z"/>
      </svg>
    </a>
    <a href="https://www.linkedin.com/in/sahar-osman-a19a45209/" target="_blank" rel="noopener">
      linkedin.com/in/sahar-osman-a19a45209/
    </a>
  </div>

  <div class="sep"></div>

  <div class="row">📍 مدرسة عثمان بن عفّان النموذجية للبنين</div>
  <div class="row">وزارة التعليم والتعليم العالي – دولة قطر</div>

  <div class="sep"></div>

  <div class="fine">© 2025 جميع الحقوق محفوظة – <strong>إنجاز</strong> | Developed with ❤️ in Qatar</div>
</div>
"""

def render_footer():
    """Render the Injaz footer component."""
    st.markdown(FOOTER_HTML, unsafe_allow_html=True)

