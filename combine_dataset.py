from pathlib import Path
import shutil

# Paths
potazos = Path(r"V:\RetailAI\dataset")
maggi = Path(r"G:\maggi.v1i.yolov12")
output = Path(r"V:\RetailAI\combined_dataset")

# Classes
# 0 = potazos
# 1 = maggi

for split in ["train", "valid", "test"]:
    out_images = output / split / "images"
    out_labels = output / split / "labels"

    out_images.mkdir(parents=True, exist_ok=True)
    out_labels.mkdir(parents=True, exist_ok=True)

    # ---------- POTAZOS ----------
    p_img = potazos / split / "images"
    p_lbl = potazos / split / "labels"

    for img in p_img.iterdir():
        if img.is_file():
            shutil.copy2(img, out_images / f"potazos_{img.name}")

    for lbl in p_lbl.glob("*.txt"):
        new_lines = []

        for line in lbl.read_text().splitlines():
            parts = line.split()

            if len(parts) == 5:
                parts[0] = "0"
                new_lines.append(" ".join(parts))

        (out_labels / f"potazos_{lbl.name}").write_text(
            "\n".join(new_lines) + "\n"
        )

    # ---------- MAGGI ----------
    m_img = maggi / split / "images"
    m_lbl = maggi / split / "labels"

    for img in m_img.iterdir():
        if img.is_file():
            shutil.copy2(img, out_images / f"maggi_{img.name}")

    for lbl in m_lbl.glob("*.txt"):
        new_lines = []

        for line in lbl.read_text().splitlines():
            parts = line.split()

            if len(parts) == 5:
                # Both Maggi classes become class 1
                parts[0] = "1"
                new_lines.append(" ".join(parts))

        (out_labels / f"maggi_{lbl.name}").write_text(
            "\n".join(new_lines) + "\n"
        )

# Create data.yaml
yaml = """path: V:/RetailAI/combined_dataset

train: train/images
val: valid/images
test: test/images

nc: 2

names:
  0: potazos
  1: maggi
"""

(output / "data.yaml").write_text(yaml)

print("===================================")
print(" Combined dataset created!")
print("===================================")
print("Location:", output)
print("Classes:")
print("0 = potazos")
print("1 = maggi")