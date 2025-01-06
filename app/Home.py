import streamlit as st

# Set page configuration
st.set_page_config(page_title="Social Media Analytics", layout="wide", initial_sidebar_state="collapsed")

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
         @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap');
        body {
            background: #F8F9FA;
            color: #333333;  /* Default text color (light mode) */
            font-family: 'Arial', sans-serif;
        }

        /* Dark mode adjustments */
        [data-theme="dark"] {
            background: #1A202C;
            color: #E2E8F0;  /* Light text color in dark mode */
        }

        /* Header Container Styling */
        .header {
            padding: 40px 20px;
            text-align: center;
            border-radius: 20px;
        }

        .header-text {
            font-size: 6vw;
            font-weight: 600;
            color: #fff;
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(45deg, #32CD32, #00FF00);  /* Green neon gradient */
            background-clip: text;
            text-fill-color: transparent;
            text-transform: uppercase;
            letter-spacing: 4px;
            animation: glow 1.5s ease-in-out infinite alternate;
            text-shadow: 0 0 10px #00FF00, 0 0 20px #32CD32, 0 0 30px #00FF00, 0 0 40px #00FF00, 0 0 50px #32CD32;
        }

        /* Glow Animation */
        @keyframes glow {
            0% {
                text-shadow: 0 0 5px #00FF00, 0 0 10px #32CD32, 0 0 15px #00FF00, 0 0 20px #00FF00;
            }
            50% {
                text-shadow: 0 0 15px #00FF00, 0 0 30px #32CD32, 0 0 45px #00FF00, 0 0 60px #00FF00;
            }
            100% {
                text-shadow: 0 0 25px #00FF00, 0 0 50px #32CD32, 0 0 75px #00FF00, 0 0 100px #00FF00;
            }
        }

        .hero-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .hero-text {
            text-align: center;
            max-width: 600px;
            padding: 20px;
        }
        .hero-text h1 {
            font-size: 4vw;
            font-weight: bold;
            color: #7300ff; 
            background-color: #d3f9fc; 
            padding: 10px 15px; 
            border-radius: 30px; 
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .hero-text h2 {
            font-size: 3vw;
            margin-top: 10px;
        }
        .hero-text p {
            font-size: 1.5vw;
            margin-top: 15px;
        }

        /* Features section */
        .features-section {
            text-align: center;
            margin-top: 60px;
            padding: 20px;
            color: black;  /* Set text color to black for the section */
        }
        .features-section h2 {
            color: #03c105; 
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        .features-section p {
            text-shadow: 1px 1px 2px #ffffff;
            color: #31f733; 
            font-size: 1.2em;
            margin-bottom: 40px;
        }

        .features-container {
            display: grid;
            grid-template-columns: repeat(3, 1fr); /* Three items per row */
            gap: 30px;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }

        .feature-box {
            background: #ffffff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
            text-align: left;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .feature-box:hover {
            transform: translateY(-10px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
        }

        .feature-box h3 {
            color: #7300ff; 
            font-size: 1.5em;
            margin-top: 10px;
            text-align: center;
        }
        
        .feature-box p {
            color: #555555; 
            font-size: 1.1em;
            line-height: 1.6;
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


        /* Responsive design */
        @media screen and (max-width: 768px) {
            .features-container {
                grid-template-columns: 1fr 1fr;  /* 2 items per row on smaller screens */
            }
            .header-text {
                font-size: 5vw;
                letter-spacing: 2px;
            }
            .hero {
                flex-direction: column;
                align-items: center;
            }
            .hero-text {
                padding-right: 0;
            }
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
            .header {
                font-size: 10vw;
            }
            .header-text {
                font-size: 5vw;
                letter-spacing: 2px;
            }
            .hero-text h1 {
                font-size: 6vw;
            }
            .hero-text h2 {
                font-size: 4vw;
            }
            .hero-text p {
                font-size: 4vw;
            }
            .features-section h2 {
                font-size: 2em;
            }
            .footer-column h3,
            .footer-column h4 {
                font-size: 1.2em;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header with Application Name
st.markdown(
    """
    <div class="header">
        <span class="header-text">SocialAnalytics</span>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns([2, 2])

with col1:
    st.markdown(
        """
        <div class="hero-wrapper">
            <div class="hero-text">
                <h1>Powered by AI</h1>
                <h2>Unleash the Power of Social Media Analytics</h2>
                <p>Empower your growth with AI-driven insights designed to boost engagement and expand your reach.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
with col2:
    st.image("static/images/hp_image.png", use_container_width=True)

col1, col2, col3 = st.columns([2, 2, 2])

with col2:
    col_button1, col_button2 = st.columns([1, 1])

    with col_button1:
        start = st.button('Get Started 🚀', key='get_started', type="primary")
        if start:
            st.switch_page("pages/Chat.py")

    with col_button2:
        st.link_button(
            'View Demo 📺',
            url=f"https://www.youtube.com/watch?v=gtmDI0b8U-Q",
        )

# Features Section with updated titles and descriptions
st.markdown(
    """
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
    <div class="features-section">
        <h2>Revolutionary Analytics Dashboard</h2>
        <p>Use AI-powered tools to enhance and simplify your social media management.</p>
        <div class="features-container" style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: center;">
            <div class="feature-box" style="width: 30%; text-align: center;">
                <i class="fas fa-chart-line" style="font-size: 40px; color: #6C63FF;"></i>
                <h3>Instant Data Monitoring</h3>
                <p>Access up-to-the-minute metrics to make quick, informed decisions and improve strategies.</p>
            </div>
            <div class="feature-box" style="width: 30%; text-align: center;">
                <i class="fas fa-globe" style="font-size: 40px; color: #6C63FF;"></i>
                <h3>Global Audience Insights</h3>
                <p>Analyze and gain insights from your audience worldwide to tailor your content effectively.</p>
            </div>
            <div class="feature-box" style="width: 30%; text-align: center;">
                <i class="fas fa-comments" style="font-size: 40px; color: #6C63FF;"></i>
                <h3>Automated Engagement Tips</h3>
                <p>AI-powered suggestions to engage your followers more effectively and boost growth.</p>
            </div>
            <div class="feature-box" style="width: 30%; text-align: center;">
                <i class="fas fa-tools" style="font-size: 40px; color: #6C63FF;"></i>
                <h3>Post Optimization Tools</h3>
                <p>Maximize engagement through intelligent recommendations for content improvement.</p>
            </div>
            <div class="feature-box" style="width: 30%; text-align: center;">
                <i class="fas fa-robot" style="font-size: 40px; color: #6C63FF;"></i>
                <h3>Efficient Task Automation</h3>
                <p>Automate your social media tasks to save time and focus on creative strategies.</p>
            </div>
            <div class="feature-box" style="width: 30%; text-align: center;">
                <i class="fas fa-user" style="font-size: 40px; color: #6C63FF;"></i>
                <h3>In-depth User Behavior Analysis</h3>
                <p>Understand user actions and preferences to build stronger, more personalized connections.</p>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


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
            <p>Email: <a href="mailto:developxdave@gmail.com">developxdave@gmail.com</a></p>
            <p>Developed by: Lentreo</p>
            <p>© 2025 SocialAnalytics. All rights reserved.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
