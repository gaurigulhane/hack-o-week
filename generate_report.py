import os
import sys

# Project Data
projects = [
    {
        "title": "Week 1: Peak Hour Electricity Spikes",
        "image": "Week-1-Peak-Hour-Electricity-Spikes/screenshots/skeuo_main.png",
        "repo": "https://github.com/DevDhapodkar/Peak-Hour-Electricity-Spikes-Prediction-Dashboard",
        "desc": "Collect hourly meter data from dorms; apply moving average smoothing and linear regression to predict evening peaks based on past week. Visualize trends on a live Plotly dashboard."
    },
    {
        "title": "Week 2: Classroom Usage Forecasting",
        "image": "Week-2-Classroom-Usage-Forecasting/assets/dashboard.png",
        "repo": "https://github.com/DevDhapodkar/Classroom-Usage-Forecasting-Walkthrough",
        "desc": "Use sensor data (occupancy via Wi-Fi logs) to train a simple ARIMA model for next-hour room electricity draw; dashboard shows confidence intervals."
    },
    {
        "title": "Week 3: Library Energy During Exams",
        "image": "Week-3-Library-Energy-Forecast/screenshots/dashboard_finals.png",
        "repo": "https://github.com/DevDhapodkar/Library-Energy-Forecast-During-Exams",
        "desc": "Aggregate historical usage with event calendars; implement exponential smoothing for semester-end forecasts, displayed as a gauge on Streamlit dashboard."
    },
    {
        "title": "Week 4: Cafeteria Load Prediction",
        "image": "Week-4-Cafeteria-Load-Prediction/assets/screenshot.png",
        "repo": "https://github.com/DevDhapodkar/Cafeteria-Load-Prediction-Tasks",
        "desc": "Predict lunch-hour surges using temperature/weather data and linear regression; real-time line chart updates via WebSocket integration."
    },
    {
        "title": "Week 5: HVAC Optimization in Labs",
        "image": "Week-5-HVAC-Optimization/assets/heatmap_view.png",
        "repo": "https://github.com/DevDhapodkar/HVAC-Optimization-in-Labs",
        "desc": "Train a basic decision tree on occupancy/temperature data to forecast cooling needs; dashboard with heatmaps for zone-wise predictions."
    },
    {
        "title": "Week 6: Sports Facility Night Usage",
        "image": "Week-6-Sports-Facility-Usage/assets/dashboard_all_days_1772692155394.png",
        "repo": "https://github.com/DevDhapodkar/Sports-Facility-Night-Usage",
        "desc": "Use RNN (simple LSTM) on hourly patterns to predict post-event electricity; interactive dashboard filters by day type."
    },
    {
        "title": "Week 7: Admin Building Weekend Dip",
        "image": "Week-7-Admin-Building-Analysis/assets/dashboard.png",
        "repo": "https://github.com/DevDhapodkar/Admin-Building-Weekend-Dip",
        "desc": "Apply k-means clustering on usage profiles then regress clusters for forecasts; pie charts show savings potential on dashboard."
    },
    {
        "title": "Week 8: Parking Lot Lighting Forecast",
        "image": "Week-8-Parking-Lot-Lighting-Forecast/screenshot.png",
        "repo": "https://github.com/DevDhapodkar/Parking-Lot-Lighting-Forecast",
        "desc": "Uses sensor-based vehicle count data with polynomial regression for light usage. Real-time bar chart with anomaly alerts."
    },
    {
        "title": "Week 9: Hostel Laundry Peak Prediction",
        "image": "Week-9-Hostel-Laundry-Peak-Prediction/screenshot.png",
        "repo": "https://github.com/DevDhapodkar/Hostel-Laundry-Peak-Prediction",
        "desc": "Time-series data with naive Bayes for usage categories; forecasting with Prophet. Dashboard with timeline slider for what-if scenarios."
    },
    {
        "title": "Week 10: Campus-Wide Sustainability Tracker",
        "image": "Week-10-Campus-Wide-Sustainability-Tracker/screenshot.png",
        "repo": "https://github.com/DevDhapodkar/Campus-Wide-Sustainability-Tracker",
        "desc": "Ensemble basic models (regression + smoothing) on aggregated data. Comprehensive dashboard with KPIs like carbon savings."
    },
    {
        "title": "Week 11: User Registration Portal",
        "image": "Week-11-User-Registration-Portal/screenshot.png",
        "repo": "https://github.com/DevDhapodkar/User-Registration-Portal",
        "desc": "Secure wearable data management with JWT authentication and AES-256 encryption. React interface for synchronization and profile decryption."
    },
]

def generate_report():
    from fpdf import FPDF
    
    class ProjectPDF(FPDF):
        def header(self):
            self.set_font('helvetica', 'B', 15)
            self.cell(0, 10, 'Hack-o-week Projects Report', border=False, align='C')
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font('helvetica', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', align='C')

    pdf = ProjectPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Title Page
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 25)
    pdf.ln(60)
    pdf.cell(0, 20, 'Hack-o-week Projects', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('helvetica', '', 15)
    pdf.cell(0, 10, 'Consolidated Energy & Utility Forecasting Solutions', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)
    pdf.cell(0, 10, f'Date: 2026-03-12', align='C', new_x="LMARGIN", new_y="NEXT")
    
    for project in projects:
        title = project["title"]
        img_path = project["image"]
        repo_link = project["repo"]
        desc = project["desc"]
        
        if os.path.exists(img_path):
            pdf.add_page()
            
            # Project Title
            pdf.set_font('helvetica', 'B', 18)
            pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(5)
            
            # Project Description
            pdf.set_font('helvetica', '', 11)
            pdf.multi_cell(0, 6, desc)
            pdf.ln(3)
            
            # Repository Link
            pdf.set_font('helvetica', 'I', 10)
            pdf.set_text_color(0, 0, 255)
            pdf.write(5, "Repository: ")
            pdf.write(5, repo_link, repo_link)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(10)
            
            # Project Screenshot
            # Scale to fit page width (190mm)
            pdf.image(img_path, x=10, y=None, w=190)
        else:
            print(f"Warning: Image not found for {title}: {img_path}")

    output_path = "Hack-o-week-Projects-Report.pdf"
    pdf.output(output_path)
    print(f"Report generated successfully: {output_path}")

if __name__ == "__main__":
    generate_report()
