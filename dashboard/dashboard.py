import pandas as pd
import streamlit as st
import altair as alt

def create_monthly_counts_df(day_df):
    day_df['year_month'] = day_df['dteday'].dt.to_period('M')
    monthly_counts = day_df.groupby('year_month')['cnt'].sum()

    return monthly_counts

def create_season_counts_df(day_df):
    season_counts = day_df.groupby('season')['cnt'].sum().rename(index={1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})

    return season_counts

def create_user_sum_df(day_df):
    casual_sum = day_df['casual'].sum()
    registered_sum = day_df['registered'].sum()

    sum_df = pd.DataFrame({'User Type': ['Casual', 'Registered'],
                        'Sum': [casual_sum, registered_sum]})

    return sum_df

def create_day_counts_df(day_df):
    dayoff_counts = day_df[day_df['workingday'] == 0]['cnt'].sum()
    workingday_counts = day_df[day_df['workingday'] == 1]['cnt'].sum()

    counts_df = pd.DataFrame({'Day Type': ['Weekend/Holiday', 'Working Day'],
                            'Counts': [dayoff_counts, workingday_counts]})

    return counts_df

day_df = pd.read_csv("dashboard/day.csv")

day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)

day_df["dteday"] = pd.to_datetime(day_df["dteday"])

# Filter data
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    # Foto
    st.image("https://media.licdn.com/dms/image/D5603AQE_-wvzWdZqqw/profile-displayphoto-shrink_800_800/0/1675864948980?e=2147483647&v=beta&t=1I_nolkFj02fN4MRs9XIH162X7422J5KqnzX1UgXFOA")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

# # Menyiapkan berbagai dataframe
monthly_counts_df = create_monthly_counts_df(main_df)
season_counts_df = create_season_counts_df(main_df)
user_type_df = create_user_sum_df(main_df)
day_counts_df = create_day_counts_df(main_df)

st.header("Dashboard Bike Sharing")

col1, col2, col3 = st.columns(3)

with col1:
    total_bike_used = main_df['cnt'].sum()
    st.metric('Total Penggunaan Bike Sharing', value=total_bike_used)

with col2:
    total_registered_user = main_df['registered'].sum()
    st.metric('Total Registered User', value=total_registered_user)

with col3:
    average_bike_used = round(main_df['cnt'].mean(), 2)
    st.metric('Mean Pengguna Bike Sharing (days)', value=average_bike_used)

monthly_counts_df.index = monthly_counts_df.index.astype(str)
st.subheader("Perkembangan Bike Sharing per Bulan")

monthly_chart = (alt.Chart(monthly_counts_df.reset_index()).mark_line(point=alt.OverlayMarkDef(filled=True)).encode(
    x=alt.X('year_month', axis=alt.Axis(labelAngle=-45), title='Tahun-Bulan'),
    y=alt.X('cnt', title='Jumlah'),
)).interactive()

st.altair_chart(
    monthly_chart.interactive(),
    use_container_width=True
)


st.subheader("Penggunaan Bike Sharing per Season")

season_counts_df.index = season_counts_df.index.astype(str)
season_chart = (alt.Chart(season_counts_df.reset_index()).mark_bar().encode(
    x=alt.X('cnt', axis=alt.Axis(labelAngle=360), title='Jumlah'),
    y=alt.X('season', title='Season', sort='-x'),
)).interactive()

st.altair_chart(
    season_chart.interactive(),
    use_container_width=True
)

st.subheader("Penggunaan Bike Sharing per User Type")
user_chart = (alt.Chart(user_type_df).mark_bar().encode(
    x=alt.X('User Type', axis=alt.Axis(labelAngle=360), title='Tipe User'),
    y=alt.X('Sum', title='Jumlah'),
)).interactive()

st.altair_chart(
    user_chart.interactive(),
    use_container_width=True
)

st.subheader("Penggunaan Bike Sharing: Hari Kerja vs Liburan")

day_chart = (alt.Chart(day_counts_df).mark_bar().encode(
    x=alt.X('Day Type', axis=alt.Axis(labelAngle=360), title='Hari'),
    y=alt.Y('Counts', title='Jumlah')
)).interactive()

st.altair_chart(
    day_chart.interactive(),
    use_container_width=True
)

st.caption('Lingga Rohadyan made for Dicoding submission')