import os
import txt_to_csv as t2c

if __name__ == "__main__":
    data_dir = "./data"
    merged_txt_file = os.path.join(data_dir, "combined_data_all.txt")
    merged_csv_file = os.path.join(data_dir, "combined_data_all.csv")

    t2c.txt_to_csv(merged_txt_file, merged_csv_file)

    # Manja baza podataka za testiranje tokom razvoja
    merged_csv_file = os.path.join(data_dir, "combined_data_sample.csv")

    t2c.txt_to_csv_sample(merged_txt_file, merged_csv_file, 100000)