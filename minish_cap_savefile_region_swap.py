import sys

def detect_and_convert_region(input_file, output_file):
    # Offsets and corresponding USA/PAL values
    region_diffs = [
        (25, 53, 51), (36, 26, 25), (38, 229, 230), (112, 1, 2),
        (4121, 53, 51), (4132, 26, 25), (4134, 229, 230), (4208, 1, 2)
    ]
    
    with open(input_file, "rb") as f:
        save_data = bytearray(f.read())
    
    # Determine region
    is_usa = all(save_data[off] == usa_val for off, usa_val, pal_val in region_diffs)
    is_pal = all(save_data[off] == pal_val for off, usa_val, pal_val in region_diffs)
    
    if not (is_usa or is_pal):
        print("Unknown or modified save file format. Cannot determine region.")
        return
    
    # Convert region
    for off, usa_val, pal_val in region_diffs:
        save_data[off] = pal_val if is_usa else usa_val
    
    # Save output with explicit region in filename
    output_region = "PAL" if is_usa else "USA"
    output_file = input_file.replace(".sav", f"_{output_region}.sav")
    
    with open(output_file, "wb") as f:
        f.write(save_data)
    
    print(f"Successfully converted to {output_region} region. Saved as {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python gba_save_region_swapper.py <input_save.sav>")
        sys.exit(1)
    
    input_save = sys.argv[1]
    detect_and_convert_region(input_save, input_save)
