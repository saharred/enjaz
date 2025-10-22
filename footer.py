import streamlit as st

FOOTER_HTML = """
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
<style>
  .injaz-footer{
    direction: rtl; 
    text-align: center; 
    font-family: 'Cairo', 'Segoe UI', system-ui, sans-serif;
    background: #8A1538; 
    color: #fff; 
    border-radius: 20px; 
    padding: 28px 18px; 
    margin-top: 24px;
    box-shadow: 0 8px 24px rgba(0,0,0,.18);
  }
  .injaz-footer .row{
    font-size: 1rem; 
    line-height: 1.9;
    margin: 4px 0;
  }
  .injaz-footer .label{
    color: #C9A227; 
    font-weight: 600;
  }
  .injaz-footer .sep{
    width: 210px; 
    height: 3px; 
    background: #C9A227; 
    border-radius: 2px; 
    margin: 16px auto;
  }
  .injaz-footer .vision{
    font-size: 1.15rem; 
    font-weight: 600;
    opacity: 0.95; 
    margin: 12px 0;
  }
  .injaz-footer .copyright{
    font-size: 0.92rem; 
    opacity: 0.95; 
    margin-top: 12px;
  }
  .injaz-footer a{
    color: #C9A227; 
    text-decoration: none; 
    font-weight: 600; 
    border-bottom: 1px dotted rgba(201,162,39,.35);
  }
  .injaz-footer a:hover{
    color: #E5C75A; 
    border-bottom: 1px solid #E5C75A;
  }

  @media (max-width:540px){
    .injaz-footer{
      padding: 22px 14px;
    }
    .injaz-footer .sep{
      width: 160px;
    }
  }
</style>

<div class="injaz-footer">
  <!-- 1. المدرسة + الوزارة -->
  <div class="row">مدرسة عثمان بن عفّان النموذجية للبنين</div>
  <div class="row">وزارة التعليم والتعليم العالي – دولة قطر</div>
  
  <div class="sep"></div>
  
  <!-- 2. تطوير وتنفيذ -->
  <div class="row"><span class="label">تطوير وتنفيذ:</span> Sahar Osman</div>
  <div class="row"><a href="mailto:Sahar.Osman@education.qa">Sahar.Osman@education.qa</a></div>
  
  <!-- 4. فاصل -->
  <div class="sep"></div>
  
  <!-- 5. الرؤية -->
  <div class="vision">"متعلّم ريادي لتنمية مستدامة"</div>
  
  <!-- 6. حقوق الملكية -->
  <div class="copyright">© 2025 جميع الحقوق محفوظة – <strong>إنجاز</strong></div>
</div>
"""

def render_footer():
    """Render the Injaz footer component."""
    st.markdown(FOOTER_HTML, unsafe_allow_html=True)

