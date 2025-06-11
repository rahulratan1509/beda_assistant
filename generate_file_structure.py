import os

def generate_tree(root_dir, prefix=""):
    lines = []
    items = sorted(os.listdir(root_dir))
    for index, item in enumerate(items):
        path = os.path.join(root_dir, item)
        connector = "└── " if index == len(items) - 1 else "├── "
        lines.append(prefix + connector + item)
        if os.path.isdir(path):
            extension = "    " if index == len(items) - 1 else "│   "
            lines += generate_tree(path, prefix + extension)
    return lines

if __name__ == "__main__":
    root_directory = "."  # Current directory, or replace with your project path
    output_file = "project_structure.txt"

    tree_lines = [os.path.basename(os.path.abspath(root_directory)) + "/"]
    tree_lines += generate_tree(root_directory)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(tree_lines))

    print(f"✅ File structure saved to '{output_file}'")
