import csv

def create_csv_with_second_column(input_file, output_file):
    with open(input_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Salta la prima riga (l'intestazione) se presente

        data_to_write = []
        for row in reader:
            if len(row) >= 2:
                data_to_write.append([row[1]])  # Aggiunge solo il dato della seconda colonna

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data_to_write)

if __name__ == "__main__":
    input_csv_filename = "/Users/aleg2/Desktop/real_5.csv"  # Inserisci il nome del file CSV di partenza
    output_csv_filename = "/Users/aleg2/Desktop/real_5_clean.csv"  # Inserisci il nome del file CSV di destinazione

    create_csv_with_second_column(input_csv_filename, output_csv_filename)
