# chat_with_detective.py
import requests
import time
import uuid

# The webhook URLs for your running agents
COLLECTOR_ENDPOINT = "http://127.0.0.1:8003/submit_tip"
DETECTIVE_ENDPOINT = "http://127.0.0.1:8002/get_report"

def print_report(report_data: dict):
    """Prints the detective's report in a clean format."""
    print("\n" + "═"*80)
    print("DETECTIVE'S SYNTHESIS:")
    print("─"*80)
    print(f"CASE SUMMARY: {report_data.get('case_summary')}\n")
    print(f"AI SYNTHESIS:\n{report_data.get('ai_synthesis')}")
    print("═"*80 + "\n")

def main():
    """Main function to run the interactive chat loop."""
    print("Starting session with the detective unit.")
    
    # Generate a unique case ID for this session
    case_id = str(uuid.uuid4())
    print(f"Opened new case file: {case_id}")
    
    while True:
        try:
            # Get input from the user
            tip = input("Your Message (or type 'exit' to quit): ")
            if tip.lower() == 'exit':
                print("Ending session.")
                break

            # 1. Send the tip to the Evidence Collector
            print("Sending message to the collector...")
            submit_payload = {"case_id": case_id, "text": tip}
            response = requests.post(COLLECTOR_ENDPOINT, json=submit_payload, timeout=10)
            
            if response.status_code != 200 or response.json().get('status') != 'success':
                print(f"Error submitting tip: {response.text}")
                continue

            # 2. Poll the Detective for the updated report
            print("Waiting for detective's analysis...")
            for _ in range(10):  # Poll for up to 50 seconds (10 * 5s)
                time.sleep(5)
                report_response = requests.get(f"{DETECTIVE_ENDPOINT}/{case_id}", timeout=10)
                
                if report_response.status_code == 200:
                    data = report_response.json()
                    if data.get('status') == 'complete':
                        print_report(data.get('report'))
                        break # Exit the polling loop on success
            else: # This 'else' belongs to the 'for' loop
                print("The detective did not produce a report in time.")

        except requests.exceptions.RequestException as e:
            print(f"\nConnection Error: Failed to reach the agent system. Ensure both agents are running. Details: {e}")
        except KeyboardInterrupt:
            print("\nEnding session.")
            break

if __name__ == "__main__":
    main()
