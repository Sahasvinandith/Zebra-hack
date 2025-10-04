import subprocess, time, os

print("Starting Project Sentinel Engine...")
engine = subprocess.Popen(["uvicorn", "src.engine.api:app", "--reload", "--port", "8000"])

time.sleep(2)

print("Streaming test data...")
test_file = "data/input/rfid.jsonl"
if os.path.exists(test_file):
    subprocess.run(["python", "src/clients/python_client.py", test_file, "rfid"])
else:
    print("No test data found at", test_file)

engine.terminate()
