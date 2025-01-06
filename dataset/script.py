import csv
import uuid
import random
from datetime import datetime, timedelta

post_types = ["Carousel", "Reels", "Static"]
post_categories = ["Travel", "Food", "Tech", "Fashion"]
engagement_data = {
    'Carousel': {'likes': (200, 500), 'shares': (50, 150), 'comments': (30, 100)},
    'Reels': {'likes': (300, 700), 'shares': (100, 300), 'comments': (50, 200)},
    'Static': {'likes': (50, 200), 'shares': (10, 50), 'comments': (5, 30)}
}

num_rows = 500

def random_date(start, end):
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + timedelta(days=random_days)

def small_uuid():
    return str(uuid.uuid4())[:8] 

end_date = datetime.today()
start_date = end_date - timedelta(days=30)

data = []
for i in range(1, num_rows + 1):
    post_id = small_uuid()
    post_type = random.choice(post_types)
    post_category = random.choice(post_categories)
    date_posted = random_date(start_date, end_date).strftime("%Y-%m-%d")

    likes = random.randint(*engagement_data[post_type]['likes'])
    comments = random.randint(*engagement_data[post_type]['comments'])
    shares = random.randint(*engagement_data[post_type]['shares'])
    
    # engagement_rate = round((likes + comments + shares) / (likes * 10), 2)
    data.append([post_id, post_type, post_category, date_posted, likes, comments, shares])

csv_file = "social_media_engagement.csv"
with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["PostID", "PostType", "PostCategory", "DatePosted", "Likes", "Comments", "Shares"])
    writer.writerows(data)

print(f"Dataset successfully created and saved as {csv_file}")
