import pandas as pd
from datetime import datetime

def generate_report():
    df = pd.read_csv("data/factory_data.csv")
    report_name = f"factory_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(report_name, index=False)
    print(f"Report saved as {report_name}")

if __name__ == "__main__":
    generate_report()