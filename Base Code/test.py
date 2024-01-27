

points = 200

with open("high_score.txt", "r+") as high_score_file:  # if file is empty, set score to 0
    if high_score_file.read() == "":
        print("here")
        high_score_file.write("0")

with open("high_score.txt", "r") as high_score_file:  # reads the file for the high score
    high_score = int(high_score_file.read())


if points > high_score:  # if the points the user has is greater than the high score, then it becomes the high score
    high_score = points
    with open("high_score.txt", "w") as high_score_file:
        high_score_file.write(str(high_score))


