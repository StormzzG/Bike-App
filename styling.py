import streamlit as st

style_image1 = """
width: auto;
max-width: 850px;
height: auto;
max-height: 750px;
display: block;
justify-content: center;
border-radius: 20%;
"""

style_image2 = """
width: auto;
max-width: 900px;
height: auto;
max-height: 800px;
display: block;
justify-content: center;
border-radius: 30%;
"""

st.markdown(
    f'<img src="{"https://people.com/thmb/TzDJt_cDuFa_EShaPF1WzqC8cy0=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc():focal(216x0:218x2)/michael-jordan-435-3-4fc019926b644905a27a3fc98180cc41.jpg"}" style="{style_image1}">',
    unsafe_allow_html=True,
)

st.markdown(
    f'<img src="{"https://people.com/thmb/TzDJt_cDuFa_EShaPF1WzqC8cy0=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc():focal(216x0:218x2)/michael-jordan-435-3-4fc019926b644905a27a3fc98180cc41.jpg"}" style="{style_image2}">',
    unsafe_allow_html=True,
)