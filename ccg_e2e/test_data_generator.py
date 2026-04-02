
path = "/Users/dusanzoric/Projects/store-ordering-svc/db/changelog/tenant"



import os

# -------- CONFIGURATION --------
INPUT_FOLDER = path              # folder containing your XML files
OUTPUT_FILE = "merged_xml_output.xml"  # output file name
SEPARATOR_FORMAT = "\n\n<!-- ===== FILE: {filename} ===== -->\n\n"
# --------------------------------


def merge_xml_files(input_folder, output_file):
    # Collect all .xml files
    xml_files = sorted(
        f for f in os.listdir(input_folder)
        if f.lower().endswith(".xml")
    )

    if not xml_files:
        print("No XML files found in folder:", input_folder)
        return

    with open(output_file, "w", encoding="utf-8") as outfile:
        for xml_file in xml_files:
            file_path = os.path.join(input_folder, xml_file)

            # Write separator with filename
            outfile.write(SEPARATOR_FORMAT.format(filename=xml_file))

            # Append the content of the XML file
            with open(file_path, "r", encoding="utf-8") as infile:
                outfile.write(infile.read())

    print(f"Done! Merged {len(xml_files)} XML files into: {output_file}")


if __name__ == "__main__":
    merge_xml_files(INPUT_FOLDER, OUTPUT_FILE)