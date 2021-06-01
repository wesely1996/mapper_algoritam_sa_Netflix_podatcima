import os

def txt_to_csv(from_file, to_file):
    movie_id = None
    with open(merged_csv_file, "w") as csv_f:
        with open(merged_txt_file, "r") as txt_f:
            csv_f.write('MovieID,CustomerID,Rating,Date\n')
            for line in txt_f:
                line_split = line.split(",")

                if len(line_split) == 1:
                    movie_id = line.replace(":", "")
                    movie_id = movie_id.replace("\n", "")
                    movie_id = movie_id.replace("\r\n", "")
                else:
                    line = movie_id + "," + line
                    csv_f.write(line)

def txt_to_csv_sample(from_file, to_file, amount):
    movie_id = None
    with open(merged_csv_file, "w") as csv_f:
        with open(merged_txt_file, "r") as txt_f:
            csv_f.write('MovieID,CustomerID,Rating,Date\n')
            for line in txt_f:
                line_split = line.split(",")

                if len(line_split) == 1:
                    movie_id = line.replace(":", "")
                    movie_id = movie_id.replace("\n", "")
                    movie_id = movie_id.replace("\r\n", "")
                else:
                    line = movie_id + "," + line
                    csv_f.write(line)

                if amount <= 0:
                    break
                amount -= 1


if __name__ == "__main__":
    data_dir = "./data"
    merged_txt_file = os.path.join(data_dir, "combined_data_all.txt")
    merged_csv_file = os.path.join(data_dir, "combined_data_all.csv")

    txt_to_csv(merged_txt_file, merged_csv_file)

    # Manja baza podataka za testiranje tokom razvoja
    merged_csv_file = os.path.join(data_dir, "combined_data_sample.csv")

    txt_to_csv_sample(merged_txt_file, merged_csv_file, 100000)
