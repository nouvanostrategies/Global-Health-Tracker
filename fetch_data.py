import json
import urllib.request

# Fiscal Data API endpoint for Monthly Treasury Statement (MTS) or USAspending account balances
API_URL = (
    "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/"
    "v1/accounting/mts/mts_table_9"
    "?filter=record_date:gte:2024-10-01"
    "&sort=-record_date"
    "&page[size]=100"
)

def fetch_monthly_ghp_data():
    req = urllib.request.Request(API_URL, headers={"User-Agent": "Mozilla/5.0"})
    
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            records = res_data.get("data", [])
            
            # Format output for your site's chart
            output = {
                "last_updated": records[0].get("record_date") if records else "N/A",
                "monthlySpending": [
                    {
                        "date": r.get("record_date"),
                        "agency": r.get("line_code_desc"),
                        "outlays": r.get("current_month_gross_outlay_amt")
                    }
                    for r in records[:12]  # Keep most recent 12 entries
                ]
            }
            
            # Save data to data.json
            with open("data.json", "w") as f:
                json.dump(output, f, indent=2)
                
            print("Successfully updated data.json")
            
    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    fetch_monthly_ghp_data()
