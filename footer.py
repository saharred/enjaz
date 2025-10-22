import streamlit as st

FOOTER_HTML = """
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
<style>
  .injaz-footer{
    direction: rtl; 
    text-align: center; 
    font-family: 'Cairo', 'Segoe UI', system-ui, sans-serif;
    background: linear-gradient(135deg, #8A1538 0%, #6B0F2A 100%);
    color: #fff; 
    border-radius: 35px; 
    padding: 35px 25px; 
    margin-top: 32px;
    box-shadow: 0 12px 32px rgba(138, 21, 56, 0.4), 0 4px 16px rgba(201, 162, 39, 0.1);
    border-top: 4px solid #C9A227;
    position: relative;
    overflow: hidden;
  }
  .injaz-footer::before{
    content: '';
    position: absolute;
    top: -50px;
    left: -50px;
    width: 200px;
    height: 200px;
    background: radial-gradient(circle, rgba(201,162,39,0.15) 0%, transparent 70%);
    border-radius: 50%;
  }
  .injaz-footer::after{
    content: '';
    position: absolute;
    bottom: -50px;
    right: -50px;
    width: 200px;
    height: 200px;
    background: radial-gradient(circle, rgba(201,162,39,0.15) 0%, transparent 70%);
    border-radius: 50%;
  }
  .injaz-footer .row{
    font-size: 1.05rem; 
    line-height: 2;
    margin: 6px 0;
    position: relative;
    z-index: 1;
  }
  .injaz-footer .label{
    color: #E5C75A; 
    font-weight: 700;
    text-shadow: 0 2px 4px rgba(0,0,0,0.2);
  }
  .injaz-footer .sep{
    width: 220px; 
    height: 4px; 
    background: linear-gradient(90deg, transparent 0%, #C9A227 50%, transparent 100%); 
    border-radius: 3px; 
    margin: 20px auto;
    position: relative;
    z-index: 1;
    box-shadow: 0 2px 8px rgba(201,162,39,0.3);
  }
  .injaz-footer .vision{
    font-size: 1.25rem; 
    font-weight: 700;
    opacity: 1; 
    margin: 16px 0;
    position: relative;
    z-index: 1;
    text-shadow: 0 2px 6px rgba(0,0,0,0.3);
    color: #FFFFFF;
  }
  .injaz-footer .copyright{
    font-size: 0.95rem; 
    opacity: 1; 
    margin-top: 16px;
    position: relative;
    z-index: 1;
    font-weight: 600;
  }
  .injaz-footer a{
    color: #E5C75A; 
    text-decoration: none; 
    font-weight: 700; 
    border-bottom: 2px dotted rgba(229,199,90,.5);
    transition: all 0.3s ease;
    position: relative;
  }
  .injaz-footer a:hover{
    color: #FFD700; 
    border-bottom: 2px solid #FFD700;
    text-shadow: 0 0 8px rgba(255,215,0,0.5);
  }

  /* Tablet (768px and below) */
  @media (max-width: 768px){
    .injaz-footer{
      padding: 28px 20px;
      border-radius: 25px;
    }
    .injaz-footer .row{
      font-size: 1rem;
      line-height: 1.8;
    }
    .injaz-footer .sep{
      width: 180px;
      height: 3px;
      margin: 16px auto;
    }
    .injaz-footer .vision{
      font-size: 1.15rem;
    }
    .injaz-footer .copyright{
      font-size: 0.9rem;
    }
  }
  
  /* Mobile (540px and below) */
  @media (max-width: 540px){
    .injaz-footer{
      padding: 20px 16px;
      border-radius: 20px;
      margin-top: 24px;
      border-top-width: 3px;
    }
    .injaz-footer::before,
    .injaz-footer::after{
      width: 150px;
      height: 150px;
    }
    .injaz-footer .row{
      font-size: 0.95rem;
      line-height: 1.7;
      margin: 4px 0;
    }
    .injaz-footer .label{
      font-size: 0.95rem;
    }
    .injaz-footer .sep{
      width: 140px;
      height: 3px;
      margin: 14px auto;
    }
    .injaz-footer .vision{
      font-size: 1.05rem;
      margin: 12px 0;
    }
    .injaz-footer .copyright{
      font-size: 0.85rem;
      margin-top: 12px;
    }
    .injaz-footer a{
      font-size: 0.9rem;
      border-bottom-width: 1.5px;
    }
  }
  
  /* Small Mobile (400px and below) */
  @media (max-width: 400px){
    .injaz-footer{
      padding: 18px 12px;
      border-radius: 16px;
    }
    .injaz-footer .row{
      font-size: 0.9rem;
      line-height: 1.6;
    }
    .injaz-footer .sep{
      width: 120px;
      height: 2px;
      margin: 12px auto;
    }
    .injaz-footer .vision{
      font-size: 1rem;
    }
    .injaz-footer .copyright{
      font-size: 0.8rem;
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
  <div class="row" style="font-size: 0.95rem; color: #E5C75A; font-weight: 600; margin-top: 2px;">E-Learning Projects Coordinator</div>
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

