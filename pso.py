# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
from snowflake.snowpark.functions import when_matched

# Write directly to the app
st.title(f"Pending Smoothie Orders :cup_with_straw:")
st.write("Orders that need to be filled")

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.orders").filter((col('ORDER_FILLED') == 'FALSE')) 
#st.data_editor(my_dataframe,hide_index=True)
#st.write(my_dataframe.count())

if my_dataframe.count() > 0:
    editable_df = st.data_editor(my_dataframe) #,hide_index=True)
    submitted = st.button('Submit')
    if submitted:
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)

        try:
            og_dataset.merge(edited_dataset
                     , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                     , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                    )
            st.success('Someone clicked the button', icon = '👍')
        except:
            st.write('Something went wrong!')

else:
    st.success('There are no pending orders',  icon = '👍')
