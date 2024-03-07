import os
from datetime import datetime
import plotly.express as px

def get_image_dates(image_folder):
    image_dates = []
    for filename in os.listdir(image_folder):
        if filename.endswith(".jpg"):
            try:
                # Extract date information from the image name
                date_str = filename.split('-')[1][:8]
                date_obj = datetime.strptime(date_str, "%Y%m%d")
                image_dates.append(date_obj)
            except (ValueError, IndexError):
                pass  # Ignore files with incorrect naming format
    return image_dates

def plot_interactive_bar_chart(image_folder):
    image_dates = get_image_dates(image_folder)
    image_dates.sort()

    date_counts = {date: image_dates.count(date) for date in set(image_dates)}

    data = {'Date': list(date_counts.keys()), 'Number of Images': list(date_counts.values())}
    data_sorted = {'Date': sorted(data['Date']), 'Number of Images': [date_counts[date] for date in sorted(data['Date'])]}
    
    fig = px.bar(data_sorted, x='Date', y='Number of Images', title='Image Count Per Day')
    fig.update_xaxes(type='category')  # Ensure x-axis treats dates as categories
    fig.update_layout(hovermode='x')  # Show tooltips on hover

    fig.show()

# Replace 'your_image_folder_path' with the actual path to your image folder
plot_interactive_bar_chart('/media/abhi/T7')



