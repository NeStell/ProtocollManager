import os
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO

# cartelle
folders = {
    "acquisti_da_protocollare": "acquisti_protocollate",
    "vendite_da_protocollare": "vendite_protocollate"
}

# sottocartelle
subfolders = [
    "fattura_normale",
    "fattura_elettronica",
    "ordine"
]

# last_protocol_number_<main>_<sub>.txt

# riceviamo l'ultimo numero di protocollo
def protocol_file_name(main_folder, subfolder):
    """Return a safe filename for storing the counter for a given main_folder and subfolder."""
    main_safe = main_folder.replace(os.sep, "_").replace(" ", "_")
    sub_safe = subfolder.replace(os.sep, "_").replace(" ", "_")
    return f"last_protocol_number_{main_safe}_{sub_safe}.txt"


def get_last_protocol_number(main_folder, subfolder):
    """Return the last protocol number for the given main folder and subfolder."""
    protocol_file = protocol_file_name(main_folder, subfolder)

    if not os.path.exists(protocol_file):
        with open(protocol_file, "w") as f:
            f.write("0")
        return 0

    with open(protocol_file, "r") as f:
        try:
            return int(f.read())
        except ValueError:
            return 0

# salviamo nuovo numero
def save_last_protocol_number(main_folder, subfolder, number):
    protocol_file = protocol_file_name(main_folder, subfolder)
    with open(protocol_file, "w") as f:
        f.write(str(number))

# aggiungiamo protocollo nel pdf
def add_protocol_to_pdf(input_pdf_path, output_pdf_path, protocol_number, date, doc_type, subfolder):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    for page_num in range(len(reader.pages)):
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)

        # posizione e testo
        text = f"Protocollo N° {protocol_number} | Data: {date} | {doc_type}"
        if subfolder == "fattura_elettronica":
            font_size = 12
            x = 28
            y = 40 
        elif subfolder == "fattura_normale":
            font_size = 10
            x = 28
            y = 750
        else:
            font_size = 12
            x = 28
            y = 750

        can.setFont("Helvetica-Bold", font_size)
        can.drawString(x, y, text)
        can.save()

        packet.seek(0)
        overlay_pdf = PdfReader(packet)
        overlay_page = overlay_pdf.pages[0]

        original_page = reader.pages[page_num]
        original_page.merge_page(overlay_page)
        writer.add_page(original_page)

    with open(output_pdf_path, "wb") as f:
        writer.write(f)

# main
def process_pdfs():
    today = datetime.today().strftime("%d/%m/%Y")

    for main_folder, output_root in folders.items():
        if not os.path.exists(output_root):
            os.makedirs(output_root)

        for sub in subfolders:
            protocol_number = get_last_protocol_number(main_folder, sub)

            input_dir = os.path.join(main_folder, sub)
            output_dir = os.path.join(output_root, sub)

            if not os.path.exists(input_dir):
                continue

            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            for filename in os.listdir(input_dir):
                if not filename.lower().endswith(".pdf"):
                    continue

                # controllo duplicazione: se esiste file con suffisso _{filename}
                duplicate_found = False
                for existing_file in os.listdir(output_dir):
                    if existing_file.endswith(f"_{filename}"):
                        print(f"[⚠️ FitZone S.p.A]  File skippato (già protocollato): {filename} ({main_folder}/{sub})")
                        duplicate_found = True
                        break

                if duplicate_found:
                    continue

                # Protocolliamo il nuovo file
                protocol_number += 1
                input_path = os.path.join(input_dir, filename)
                output_filename = f"{protocol_number:03d}_{filename}"
                output_path = os.path.join(output_dir, output_filename)

                pretty_sub = sub.replace("_", " ").title()
                doc_type = ("Acquisto" if main_folder == "acquisti" else "Vendita") + f" - {pretty_sub}"

                add_protocol_to_pdf(input_path, output_path, protocol_number, today, doc_type, sub)
                print(f"[✅ FitZone S.p.A] Protocollato file: {filename} -> {output_filename} ({main_folder}/{sub})")


            save_last_protocol_number(main_folder, sub, protocol_number)

    print("\n[✅ FitZone S.p.A] Protocollato.\n")

# start
if __name__ == "__main__":
    process_pdfs()
