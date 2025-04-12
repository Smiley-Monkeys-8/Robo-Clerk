import os

json_path = "./data/passport_data.json"

if os.path.exists(json_path):
    print("✅ JSON file exists at:")
    print(json_path)
    
    with open(json_path, "r", encoding="utf-8") as f:
        print("\n📄 Contents of the file:\n")
        print(f.read())
else:
    print("❌ JSON file not found. Check the output path or if the write operation failed.")
