import os
import certifi
import json
from pymongo import MongoClient
from dotenv import load_dotenv


def introspect_database():
    load_dotenv()
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("DATABASE_NAME", "cs125")

    if not mongo_uri:
        print("❌ MONGO_URI not found.")
        return

    try:
        client = MongoClient(mongo_uri, tlsCAFile=certifi.where())
        db = client[db_name]

        # Ping to verify
        client.admin.command("ping")

        report = []
        report.append(f"# Database Schema Report: `{db_name}`")
        report.append(f"Generated on: 2026-02-11")
        report.append("\n## Collections Overview")

        collections = db.list_collection_names()
        if not collections:
            report.append("No collections found in this database.")
        else:
            for coll_name in collections:
                report.append(f"\n### Collection: `{coll_name}`")
                coll = db[coll_name]
                doc_count = coll.count_documents({})
                report.append(f"- **Document Count**: {doc_count}")

                # Sample a document to understand schema
                sample_doc = coll.find_one()
                if sample_doc:
                    report.append("- **Schema (Sample Structure)**:")
                    report.append("  ```json")

                    # Convert ObjectId to string for JSON serialization
                    def clean_doc(d):
                        if isinstance(d, dict):
                            return {k: clean_doc(v) for k, v in d.items()}
                        elif isinstance(d, list):
                            return [clean_doc(i) for i in d]
                        elif hasattr(d, "__str__") and "ObjectId" in str(type(d)):
                            return str(d)
                        return d

                    report.append(json.dumps(clean_doc(sample_doc), indent=4))
                    report.append("  ```")

                    # Analyze fields and types
                    report.append("- **Field Types (Detected)**:")
                    for key, value in sample_doc.items():
                        report.append(f"  - `{key}`: {type(value).__name__}")
                else:
                    report.append("- *Collection is empty.*")

        # Write to file
        output_path = "databaseScheme.md"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(report))

        print(f"✅ Schema report generated: {output_path}")

    except Exception as e:
        print(f"❌ Error during introspection: {e}")


if __name__ == "__main__":
    introspect_database()
