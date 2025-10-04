import json, time, requests, sys

def stream_file(file_path, source, delay=1.0):
    with open(file_path) as f:
        for line in f:
            event = json.loads(line)
            r = requests.post(f"http://127.0.0.1:8000/ingest/{source}", json=event)
            print("Sent:", event, "| Response:", r.json())
            time.sleep(delay)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python python_client.py <file_path> <source>")
        sys.exit(1)
    stream_file(sys.argv[1], sys.argv[2], delay=0.5)
