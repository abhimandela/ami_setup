import os
from datetime import datetime
import pandas as pd
import plotly.express as px

def get_image_dates_and_hours(image_folder):
    image_dates = []
    image_hours = []
    for filename in os.listdir(image_folder):
        if filename.endswith(".jpg"):
            try:
                # Extract date and hour information from the image name
                date_str = filename.split('-')[1][:13]
                date_obj = datetime.strptime(date_str, "%Y%m%d%H")
                image_dates.append(date_obj.date())
                image_hours.append(date_obj.hour)
            except (ValueError, IndexError):
                pass  # Ignore files with incorrect naming format
    return image_dates, image_hours

def plot_interactive_multicolored_bar_chart(image_folder):
    image_dates, image_hours = get_image_dates_and_hours(image_folder)

    data = {'Date': image_dates, 'Hour': image_hours}
    df = pd.DataFrame(data)
    
    # Count the number of images per date and hour
    df['Count'] = 1
    df_grouped = df.groupby(['Date', 'Hour']).count().reset_index()
    
    # Create a bar chart with multicolored segments
    fig = px.bar(df_grouped, x='Date', y='Count', title='Image Count Per Hour',
                 labels={'Date': 'Date', 'Count': 'Number of Images'},
                 color='Hour', color_continuous_scale='Viridis',
                 category_orders={'Hour': sorted(df['Hour'].unique())})
    
    # Customize the layout
    fig.update_xaxes(type='category')  # Ensure x-axis treats dates as categories
    fig.update_layout(hovermode='x')  # Show tooltips on hover
    
    # Add count information to the hover tooltip
    fig.update_traces(hovertemplate='Hour: %{color}<br>Number of Images: %{y}')
    
    fig.show()


# Replace 'your_image_folder_path' with the actual path to your image folder
plot_interactive_multicolored_bar_chart('/media/abhi/Vault/Test_Images_Wpi_v2')
