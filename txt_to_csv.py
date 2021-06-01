import os


if __name__ == "__main__":
    data_dir = "./data"
    merged_txt_file = os.path.join(data_dir, "combined_data_all.txt")
    merged_csv_file = os.path.join(data_dir, "combined_data_all.csv")

    movie_id = None
    with open(merged_csv_file, "w") as csv_f:
        with open(merged_txt_file, "r") as txt_f:
            for line in txt_f:
                line_split = line.split(",")

                if len(line_split) == 1:
                    movie_id = line.replace(":", "")
                    movie_id = movie_id.replace("\n", "")
                    movie_id = movie_id.replace("\r\n", "")
                else:
                    line = movie_id + "," + line
                    csv_f.write(line)
