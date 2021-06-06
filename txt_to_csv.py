def txt_to_csv(from_file, to_file):
    movie_id = None
    with open(from_file, "r") as from_f:
        with open(to_file, "w") as to_f:
            to_f.write('MovieID,CustomerID,Rating,Date\n')
            for line in from_f:
                line_split = line.split(",")

                if len(line_split) == 1:
                    movie_id = line.replace(":", "")
                    movie_id = movie_id.replace("\n", "")
                    movie_id = movie_id.replace("\r\n", "")
                else:
                    line = movie_id + "," + line
                    to_f.write(line)

def txt_to_csv_sample(from_file, to_file, amount):
    movie_id = None
    with open(from_file, "r") as from_f:
        with open(to_file, "w") as to_f:
            to_f.write('MovieID,CustomerID,Rating,Date\n')
            for line in from_f:
                line_split = line.split(",")

                if len(line_split) == 1:
                    movie_id = line.replace(":", "")
                    movie_id = movie_id.replace("\n", "")
                    movie_id = movie_id.replace("\r\n", "")
                else:
                    line = movie_id + "," + line
                    to_f.write(line)

                if amount <= 0:
                    break
                amount -= 1

