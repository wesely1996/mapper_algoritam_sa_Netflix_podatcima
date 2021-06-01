file_path_read = "./data/combined_data_all.txt"
file_path_write = "./data/combined_data.csv"

with open(file_path_read, 'r') as file:
    with open(file_path_write, 'w+') as output:
        movie_id = '0'
        for line in file:
            if line[:-2].isnumeric():
                movie_id = line[:-2]
            else:
                output.write(movie_id + ',' + line)
    output.close()
file.close()
