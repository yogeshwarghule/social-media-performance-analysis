import streamlit as st
import pandas as pd
from langflow_code import format_data, get_response_from_langflow
import plotly.express as px
import plotly.graph_objects as go
from collections import deque
import json


if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'collapsed'
# Set page configuration to wide layout
st.set_page_config(page_title="Main Application", layout="wide",  initial_sidebar_state=st.session_state.sidebar_state)


# Custom CSS for styling

st.markdown(
    """
    <style>
    /* Import Poppins font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    /* Apply font globally to the entire page */
    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
    }

    /* Optional: Customize headers */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
    }

    /* Optional: Customize paragraph and other text */
    p, span {
        font-family: 'Poppins', sans-serif;
        font-weight: 400;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
        body {
            background: var(--background);
            color: var(--text-color);
        }
        .title {
            text-align: center;
            color: var(--highlight);
            font-size: 40px;
            margin-top: 20px;
            text-transform: uppercase;
        }
        .subtitle {
            text-align: center;
            color: var(--text-color);
            font-size: 18px;
            margin-bottom: 30px;
        }
        .metrics-box {
            background: var(--box-color);
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0px 2px 10px var(--box-shadow);
        }
        .metric-title {
            font-size: 16px;
            color: var(--text-color);
        }
        .metric-value {
            color: var(--highlight);
            font-size: 28px;
            font-weight: bold;
        }
        .chart-container {
            background: var(--box-color);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0px 2px 10px var(--box-shadow);
        }
        .filter-container {
            display: flex;
            justify-content: center;
            margin-bottom: 40px;
            width: 50%;  /* Adjust the width to make it smaller */
            margin-left: auto;
            margin-right: auto;
        }
        .filter-container div {
            width: 30%;  /* Adjust the width of individual filter boxes */
        }
        /* Home button styling */
        .home-btn {
            position: absolute;
            top: 20px;
            left: 20px;
            background-color: #6C63FF;
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 16px;
            border: none;
        }
        .home-btn:hover {
            background-color: #5a53e6;
        }
        
        /* Footer Section */
        .footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 60px;
            padding: 30px;
            background: linear-gradient(145deg, #6C63FF, #A3A1FF);  /* Vibrant gradient */
            border-radius: 25px;
            color: white;
            box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.2);  /* Strong shadow for pop */
            transition: all 0.3s ease;  /* Smooth transition */
        }

        .footer:hover {
            box-shadow: 0px 20px 50px rgba(0, 0, 0, 0.3);  /* Hover effect for footer */
            transform: translateY(-5px);  /* Subtle lift on hover */
        }

        /* Footer Columns */
        .footer-column {
            flex: 1;
            text-align: center;
            margin: 0 20px;
        }

        .footer-column h3,
        .footer-column h4 {
            font-size: 1.6em;
            font-weight: 700;
            color: #ffffff;  /* Bold white headings */
            margin-bottom: 15px;
            text-transform: uppercase;  /* All caps for emphasis */
            letter-spacing: 2px;
        }

        .footer-column a {
            color: #dcdcdc;  /* Light gray text for links */
            text-decoration: none;
            font-size: 1.1em;
            margin-bottom: 12px;
            display: block;
            font-weight: 500;
            transition: color 0.3s ease, transform 0.3s ease;
        }

        /* Link Hover Effects */
        .footer-column a:hover {
            color: #6C63FF;  /* Vibrant purple color */
            transform: scale(1.05);  /* Slight zoom-in effect */
        }

        /* Social Media Icons */
        .footer-column .social-icons {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }

        .footer-column .social-icons a {
            color: #ffffff;
            margin: 0 15px;
            font-size: 1.8em;
            transition: color 0.3s ease, transform 0.3s ease;
        }

        .footer-column .social-icons a:hover {
            color: #A3A1FF;  /* Light purple hover effect */
            transform: scale(1.1);  /* Zoom-in effect on hover */
        }

        /* Responsive Footer */
        @media screen and (max-width: 768px) {
            .footer {
                flex-direction: column;
                align-items: center;
            }

            .footer-column {
                text-align: center;
                margin-bottom: 30px;
            }

            .footer-column h3,
            .footer-column h4 {
                font-size: 1.4em;
            }
        }

        @media screen and (max-width: 480px) {
            .footer-column h3,
            .footer-column h4 {
                font-size: 1.2em;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <style>
        /* Styling for buttons to ensure they do not break */
        .stButton button {
            width: 100%;  /* Make the buttons span the full width of the column */
            white-space: nowrap;  /* Prevent text wrapping */
            text-align: center;  /* Center the text */
            padding: 15px 20px;  /* Increase padding for better appearance */
            font-size: 16px;  /* Adjust font size */
        }
    </style>
    """, unsafe_allow_html=True
)

# Layout: Use two columns (left for home button, right for chat button)
col1, col2, col3 = st.columns([2, 5, 1])

# Home button in left column
with col1:
    if st.button("🏠 Home", key="home", help="Go to Home Page", use_container_width=True):
        st.switch_page("Home.py")

# Chat button in right column
with col3:
    if st.button("💬 Chat", key="chat", help="Open chat", use_container_width=True):
        st.session_state.sidebar_state = 'collapsed' if st.session_state.sidebar_state == 'expanded' else 'expanded'
        st.rerun()


# Title
st.markdown('<div class="title">Social Media Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Use filters to explore your performance metrics.</div>', unsafe_allow_html=True)

# get Initial Data
post_metadata, engagement_data, post_type_engagement_df, post_category_engagement_df, posts_df = format_data()

# Filters directly on the page (above the charts)
# col1, col2, col3 = st.columns([1,2,1])
# with col2:
#     st.markdown('<div style="padding: 20px;">', unsafe_allow_html=True)
#     start_date = st.date_input("Start Date", value=pd.to_datetime("2024-01-01"))
#     end_date = st.date_input("End Date", value=pd.to_datetime("2024-03-31"))
#     post_type = st.selectbox("Post Type", ["All Types", "Reel", "Carousel", "Static"])
#     st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    """
    <h4 style="color: var(--text-color); text-align: center; font-weight: bold;">Engagement Summary</h4>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
        .metrics-box {
            background: var(--box-color);
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0px 2px 10px var(--box-shadow);
            animation: fadeIn 1s ease-in-out;
        }
        .metric-title {
            font-size: 16px;
            color: var(--text-color);
        }
        .metric-value {
            color: var(--highlight);
            font-size: 28px;
            font-weight: bold;
            animation: bounce 1.5s infinite;
        }

        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
            40% { transform: translateY(-10px); }
            60% { transform: translateY(-5px); }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

total_likes = post_metadata.get("total_likes")
total_comments = post_metadata.get("total_comments")
total_shares = post_metadata.get("total_shares")

with kpi_col1:
    st.markdown(
        f"""
        <div class="metrics-box">
            <div class="metric-title">👍 Total Likes</div>
            <div class="metric-value">{total_likes:,} 🎉</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with kpi_col2:
    st.markdown(
        f"""
        <div class="metrics-box">
            <div class="metric-title">🔁 Total Shares</div>
            <div class="metric-value">{total_shares:,} 🔥</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with kpi_col3:
    st.markdown(
        f"""
        <div class="metrics-box">
            <div class="metric-title">💬 Total Comments</div>
            <div class="metric-value">{total_comments:,} 🚀</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Charts
st.markdown('<h4 style="color: var(--text-color); text-align: center; font-weight: bold; margin-top: 50px;">Post Distribution</h4>', unsafe_allow_html=True)
# col1, col2 = st.columns(2)

# Pie chart
reel_count = post_metadata.get("Reels")
carousel_count = post_metadata.get("Carousel")
static_count = post_metadata.get("Static")
fashion_count = post_metadata.get("fashion")
travel_count = post_metadata.get("travel")
tech_count = post_metadata.get("tech")
food_count = post_metadata.get("food")

col1, col2 = st.columns(2)
with col1:
    data = pd.DataFrame({
        "Post Type": ["Reel", "Carousel", "Static"],
        "Count": [reel_count, carousel_count, static_count],
    })


    selected_type = st.selectbox("Select Post Type for Details", ["All"] + data["Post Type"].tolist())

    if selected_type != "All":
        filtered_data = data[data["Post Type"] == selected_type]
    else:
        filtered_data = data

    # Create and display the updated chart
    fig = px.pie(
        filtered_data,
        names="Post Type",
        values="Count",
        title=f"Post Distribution - {selected_type}",
        color_discrete_sequence=px.colors.sequential.Purples_r,
    )

    st.plotly_chart(fig, use_container_width=True)
with col2:
    data = pd.DataFrame({
        "Post Category": ["Fashion", "Travel", "Tech", "Food"],
        "Count": [fashion_count, travel_count, tech_count, food_count],
    })

    selected_type = st.selectbox("Select Post Category for Details", ["All"] + data["Post Category"].tolist())

    if selected_type != "All":
        filtered_data = data[data["Post Category"] == selected_type]
    else:
        filtered_data = data

    # Create and display the updated chart
    fig = px.pie(
        filtered_data,
        names="Post Category",
        values="Count",
        title=f"Post Distribution - {selected_type}",
        color_discrete_sequence=px.colors.sequential.Greens_r,
    )

    st.plotly_chart(fig, use_container_width=True)



# Date filter inputs
st.markdown('<h4 style="color: var(--text-color); text-align: center; font-weight: bold; margin-top: 30px;">Filter by Date</h4>', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    start_date = st.date_input("Start Date", value=pd.to_datetime("2024-12-04"))
with col2:
    end_date = st.date_input("End Date", value=pd.to_datetime("2025-01-03"))

# Ensure valid date range
if start_date > end_date:
    st.error("Start date must be earlier than end date.")
else:
    # Filter data based on selected dates
    filtered_data = engagement_data[
        (engagement_data["date"] >= pd.to_datetime(start_date)) &
        (engagement_data["date"] <= pd.to_datetime(end_date))
    ]

    # Create a Plotly figure
    fig = go.Figure()

    # Add traces for likes, shares, and comments
    fig.add_trace(go.Scatter(x=filtered_data['date'], y=filtered_data['likes'], mode='lines', name='Likes', line=dict(color="#6C63FF")))
    fig.add_trace(go.Scatter(x=filtered_data['date'], y=filtered_data['shares'], mode='lines', name='Shares', line=dict(color="#4FD1C5")))
    fig.add_trace(go.Scatter(x=filtered_data['date'], y=filtered_data['comments'], mode='lines', name='Comments', line=dict(color="#ECC94B")))

    fig.update_layout(
        title="Engagement Over Time",
        xaxis_title="Date",
        yaxis_title="Count",
        legend_title="Engagement Type",
        template="plotly_dark"
    )

    st.plotly_chart(fig)


# Post Type Engagement
fig = px.bar(post_type_engagement_df,
             x='type',
             y='Average Engagement',
             color='Engagement Type',
             animation_frame='Engagement Type',
             title="Average Engagement by Post Type",
             labels={'type': 'Post Type', 'Average Engagement': 'Average Engagement'},
             template='plotly_dark')

st.plotly_chart(fig)    


# Post Category Engagement
fig2 = px.bar(post_category_engagement_df,
             x='category',
             y='Average Engagement',
             color='Engagement Type',
             animation_frame='Engagement Type',
             title="Average Engagement by Post Category",
             labels={'type': 'Post Category', 'Average Engagement': 'Average Engagement'},
             template='ggplot2')

st.plotly_chart(fig2)    


if 'messages' not in st.session_state:
    st.session_state['messages'] = deque()
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ''
if 'loading' not in st.session_state:
    st.session_state['loading'] = False
    
def get_chatbot_response(user_input):
    if user_input:
        response = get_response_from_langflow(user_input)
        return response

st.sidebar.title("InsightBot")

def handle_submit():
    if not st.session_state['loading'] and st.session_state['user_input']:
        st.session_state['loading'] = True
        st.session_state['messages'].appendleft(
            {"role": "user", "content": st.session_state['user_input']}
        )
        st.session_state['user_input'] = ""



with st.sidebar.form(key="chat_form"):
    st.text_input(
        "Type your message:",
        key="user_input",
        disabled=st.session_state['loading'],
    )
    button_label = "Send 🚀" if not st.session_state['loading'] else "Loading... ⏳"

    col1, col2= st.columns([1, 1])
    with col1:
        submit_button = st.form_submit_button(
            label=button_label,
            on_click=handle_submit,
            disabled=st.session_state['loading'],
        )
    with col2:
        clear_button = st.form_submit_button(
            label="Clear 🧹", 
            on_click=lambda: st.session_state.update({'messages': deque()}),
        )

with st.sidebar:
    f = True if len(st.session_state['messages']) >= 1 else False
    conversation_data = json.dumps(list(st.session_state['messages']), indent=4)
    st.download_button(
        disabled= not f,
        label="Download 📥",
        data=conversation_data,
        file_name="conversation_history.json",
        mime="application/json"
    )
        


# Handle response after the UI refresh
if st.session_state['loading']:
    chatbot_response = get_chatbot_response(
        st.session_state['messages'][0]["content"]
    )
    st.session_state['messages'].appendleft(
        {"role": "assistant", "content": chatbot_response}
    )
    st.session_state['loading'] = False
    st.rerun()


# Display conversation history
st.sidebar.subheader("Conversation History")
conversation_history = []

total_messages  = len(st.session_state['messages'])
for idx in range(0, total_messages, 2):
    assistant_message = st.session_state['messages'][idx]
    if idx + 1 < len(st.session_state['messages']):
        user_message = st.session_state['messages'][idx + 1]
        
        # Add user and assistant messages to history
        conversation_history.append(f"<p><strong>👤 You:</strong> {user_message['content']}</p>")
        conversation_history.append(f"<p><strong>🤖 AI:</strong> {assistant_message['content']}</p>")
        
        if idx < total_messages-2:
            # Add a separator after each pair of messages
            conversation_history.append("<hr style='border: none; border-top: 5px dashed #ccc; margin: 10px 0;'>")

st.sidebar.markdown(
    f"""
    <div style="height: 300px; overflow-y: scroll; padding: 10px; border: 1px solid #ccc; background-color: white; color: black;">
        {''.join(conversation_history)}
    </div>
    """, unsafe_allow_html=True
)


st.markdown("<div style='margin-top: 80px;'></div>", unsafe_allow_html=True)


# Table for engagement 
df = posts_df

posts_df['engagement_rate'] = round(((posts_df['likes'] + posts_df['comments'] + posts_df['shares']) / 1000) * 100, 2)

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    search_query = st.text_input("Search Table", key="search", placeholder="Search by Post ID, Post Type or Post Category")


    # Filter data based on search query (case insensitive search)
    if search_query:
        filtered_df = df[df['post_id'].str.contains(search_query, case=False) | 
                        df['type'].str.contains(search_query, case=False) | 
                        df['category'].str.contains(search_query, case=False)]
    else:
        filtered_df = df

with col2:
    # Pagination
    rows_per_page = st.selectbox("Rows per page", options=[10, 15, 20], index=1)

# Calculate the total number of pages
total_rows = len(filtered_df)
max_page = (total_rows // rows_per_page) + (1 if total_rows % rows_per_page > 0 else 0)

# Check if pagination is needed (only show pagination slider if more than one page)
with col3:
    if max_page > 1:
        page_numbers = list(range(1, max_page + 1))  # List of available page numbers
        page_number = st.selectbox("Page number", options=page_numbers, index=0)  # Default to first page
    else:
        page_number = 1 

# Slice the data for pagination
start_row = (page_number - 1) * rows_per_page
end_row = start_row + rows_per_page
post_metadata = filtered_df.iloc[start_row:end_row]

# Creating a Plotly table with a modern look
fig = go.Figure(
    data=[go.Table(
        header=dict(values=["Post ID", "Post Type", "Post Category", "Posted Date", 
                            "Likes", "Comments", "Shares", "Engagement Rate"],
                    fill_color='rgba(50, 50, 50, 0.9)',  # Dark semi-transparent gray
                    font_color='white',
                    font=dict(color='white', size=14),
                    align='center',
                    height=40),
        cells=dict(values=[post_metadata["post_id"], post_metadata["type"], post_metadata["category"],
                           post_metadata["date_posted"], post_metadata["likes"], post_metadata["comments"], 
                           post_metadata["shares"], post_metadata["engagement_rate"]],
                   fill_color='rgb(245, 245, 245)',  # Light gray for rows
                   align='center',
                   height=40,
                   font=dict(color='black', size=12),
                   line_color='rgb(233,233,233)',  # Light border between rows
                   )
    )]
)

# Set the layout for the table
fig.update_layout(
    title="Engagement Rate Table",
    title_x=0.5,
    title_font_size=22,
    width=1200,
    height=500,
    margin=dict(l=10, r=10, t=100, b=0),
    autosize=True,
    template="plotly",
)

fig.update_layout(
    title=dict(
        font=dict(size=22),
        x=0.5,
        xanchor='center', 
        yanchor='top',
    )
)

with st.container():
    st.plotly_chart(fig, use_container_width=True)

# Show total number of results and page number
st.write(f"Displaying {start_row + 1}-{min(end_row, total_rows)} of {total_rows} results.")

# Footer Section with proper alignment
st.markdown(
    """
    <div class="footer">
        <div class="footer-column">
            <h4>Quick Links</h4>
            <a href="/?page=Features">Features</a><br>
            <a href="/?page=Team">Team</a><br>
            <a href="/?page=GetStarted">Get Started</a><br>
            <a href="/?page=Contact">Contact</a>
        </div>
        <div class="footer-column">
            <h4>Contact Us</h4>
            <p>Email: <a href="mailto:yghule2001@gmail.com">yghule2001@gmail.com</a></p>
            <p>Developed by: Lentreo</p>
            <p>© 2025 SocialAnalytics. All rights reserved.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
